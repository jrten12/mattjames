import time
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse

from api.config import get_settings
from api.db import db_ping
from api.models.common import ErrorDetail, ErrorResponse
from api.observability import MetricsStore
from api.routes.approval_decisions import router as approval_decisions_router
from api.routes.admin import router as admin_router
from api.routes.apps import router as apps_router
from api.routes.client_portal import router as client_portal_router
from api.routes.demo import router as demo_router
from api.routes.founder_console import router as founder_console_router
from api.routes.intake_requests import router as intake_requests_router
from api.routes.orgs import router as orgs_router
from api.routes.preview_builds import router as preview_builds_router
from api.routes.projects import router as projects_router
from api.routes.workflow import router as workflow_router
from api.security import (
    api_auth_configured,
    api_key_fingerprint,
    api_key_is_valid,
    auth_not_configured_response,
    extract_api_key,
    invalid_api_key_response,
    missing_api_key_response,
    request_content_length_too_large,
    request_too_large_response,
)
from api.services.platform.repository import InMemoryRepository, PostgresRepository
from api.tenant_security import validate_tenant_token_for_request


def _configure_structlog() -> None:
    structlog.configure(
        processors=[structlog.processors.add_log_level, structlog.processors.TimeStamper(fmt="iso"), structlog.dev.ConsoleRenderer()],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    _configure_structlog()
    settings = get_settings()
    app.state.platform_repo = InMemoryRepository() if settings.use_inmemory_store else PostgresRepository()
    app.state.metrics_store = MetricsStore()
    yield


app = FastAPI(title="Matt James Platform", version="0.1.0", lifespan=lifespan)
http_log = structlog.get_logger("api.http")

app.include_router(orgs_router, prefix="/v1", tags=["orgs"])
app.include_router(projects_router, prefix="/v1", tags=["projects"])
app.include_router(apps_router, prefix="/v1", tags=["apps"])
app.include_router(workflow_router, prefix="/v1", tags=["workflow"])
app.include_router(demo_router, prefix="/v1", tags=["demo"])
app.include_router(intake_requests_router, prefix="/v1", tags=["intake_requests"])
app.include_router(preview_builds_router, prefix="/v1", tags=["preview_builds"])
app.include_router(approval_decisions_router, prefix="/v1", tags=["approval_decisions"])
app.include_router(admin_router, prefix="/v1", tags=["admin"])
app.include_router(client_portal_router, tags=["client_portal"])
app.include_router(founder_console_router, tags=["founder_console"])


@app.get("/admin", response_class=HTMLResponse)
async def admin_shell() -> HTMLResponse:
    html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Matt James Platform Admin</title>
  <style>
    body{font-family:Arial,sans-serif;margin:0;background:#0f1720;color:#e8edf5}
    .wrap{max-width:1080px;margin:0 auto;padding:24px}
    .hero{display:flex;justify-content:space-between;gap:20px;align-items:flex-start}
    .card{background:#1b2633;border:1px solid #2c3e50;border-radius:10px;padding:16px;margin-top:16px}
    .grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
    .stat{background:#223446;border:1px solid #38516a;border-radius:8px;padding:12px}
    button{background:#2b7fff;color:#fff;border:none;border-radius:8px;padding:10px 14px;cursor:pointer}
    input{width:100%;padding:8px;border-radius:6px;border:1px solid #4a5d71;background:#111a24;color:#eef4fb}
    label{font-size:12px;color:#a7b8cb}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    pre{background:#0d141d;border:1px solid #243344;border-radius:8px;padding:12px;overflow:auto}
    .muted{color:#a7b8cb}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div>
        <h1>Matt James Platform Admin</h1>
        <p class="muted">Demo-first admin shell for onboarding and platform operations.</p>
      </div>
      <button id="bootstrapBtn">Bootstrap Demo Org</button>
    </div>

    <div class="grid">
      <div class="stat"><div>Focus</div><strong>Core Platform</strong></div>
      <div class="stat"><div>Mode</div><strong>Demo Setup</strong></div>
      <div class="stat"><div>Workflow</div><strong>Enabled</strong></div>
      <div class="stat"><div>Environment</div><strong>Local</strong></div>
    </div>

    <div class="card">
      <h3>Demo Inputs</h3>
      <div class="row">
        <div><label>Org Name</label><input id="org_name" value="Demo Health Group"/></div>
        <div><label>Org Slug</label><input id="org_slug" value="demo-health-group"/></div>
        <div><label>Owner User ID</label><input id="owner_user_id" value="demo_owner"/></div>
        <div><label>Project Name</label><input id="project_name" value="Patient Intake Assistant"/></div>
        <div><label>App Name</label><input id="app_name" value="Intake Copilot"/></div>
        <div><label>App Slug</label><input id="app_slug" value="intake-copilot"/></div>
      </div>
    </div>

    <div class="card">
      <h3>API Settings</h3>
      <div class="row">
        <div><label>Base URL</label><input id="base_url" value="http://127.0.0.1:8000"/></div>
        <div><label>API Key</label><input id="api_key" placeholder="paste PLATFORM_API_KEYS value"/></div>
      </div>
    </div>

    <div class="card">
      <h3>Result</h3>
      <pre id="result">{ "status": "idle" }</pre>
    </div>
    <div class="card">
      <h3>Admin Controls</h3>
      <div class="row">
        <div><label>Project ID</label><input id="admin_project_id" placeholder="project uuid"/></div>
        <div><label>App ID</label><input id="admin_app_id" placeholder="app uuid"/></div>
        <div><label>Resume To State</label><input id="resume_state" value="discovery_active"/></div>
        <div><label>App Status</label><input id="app_status" value="active"/></div>
      </div>
      <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
        <button id="pauseProjectBtn">Pause Project</button>
        <button id="resumeProjectBtn">Resume Project</button>
        <button id="setAppStatusBtn">Set App Status</button>
      </div>
    </div>
  </div>
  <script>
    async function bootstrap(){
      const data = {
        org_name: document.getElementById('org_name').value,
        org_slug: document.getElementById('org_slug').value,
        owner_user_id: document.getElementById('owner_user_id').value,
        project_name: document.getElementById('project_name').value,
        app_name: document.getElementById('app_name').value,
        app_slug: document.getElementById('app_slug').value
      };
      const base = document.getElementById('base_url').value;
      const key = document.getElementById('api_key').value;
      const out = document.getElementById('result');
      out.textContent = '{ "status": "working" }';
      try{
        const res = await fetch(base + '/v1/demo/bootstrap', {
          method:'POST',
          headers:{
            'Content-Type':'application/json',
            'X-API-Key': key,
            'Idempotency-Key': 'demo-' + data.org_slug
          },
          body: JSON.stringify(data)
        });
        const json = await res.json();
        out.textContent = JSON.stringify({status: res.status, body: json}, null, 2);
      }catch(err){
        out.textContent = JSON.stringify({status: 'error', message: String(err)}, null, 2);
      }
    }
    async function adminPost(path, payload){
      const base = document.getElementById('base_url').value;
      const key = document.getElementById('api_key').value;
      const out = document.getElementById('result');
      out.textContent = '{ "status": "working" }';
      try{
        const res = await fetch(base + path, {
          method:'POST',
          headers:{
            'Content-Type':'application/json',
            'X-API-Key': key,
            'Idempotency-Key': 'admin-' + Date.now()
          },
          body: JSON.stringify(payload)
        });
        const json = await res.json();
        out.textContent = JSON.stringify({status: res.status, body: json}, null, 2);
      }catch(err){
        out.textContent = JSON.stringify({status: 'error', message: String(err)}, null, 2);
      }
    }
    document.getElementById('bootstrapBtn').addEventListener('click', bootstrap);
    document.getElementById('pauseProjectBtn').addEventListener('click', () => {
      const projectId = document.getElementById('admin_project_id').value;
      adminPost('/v1/admin/projects/' + projectId + '/pause', {});
    });
    document.getElementById('resumeProjectBtn').addEventListener('click', () => {
      const projectId = document.getElementById('admin_project_id').value;
      const toState = document.getElementById('resume_state').value;
      adminPost('/v1/admin/projects/' + projectId + '/resume', {to_state: toState});
    });
    document.getElementById('setAppStatusBtn').addEventListener('click', () => {
      const appId = document.getElementById('admin_app_id').value;
      const status = document.getElementById('app_status').value;
      adminPost('/v1/admin/apps/' + appId + '/status', {status});
    });
  </script>
</body>
</html>
"""
    return HTMLResponse(content=html)


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(_request: Request, _exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error=ErrorDetail(
                code="validation_error",
                message="Invalid request body",
                request_id=f"req_{time.time_ns()}",
            )
        ).model_dump(),
    )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readyz")
async def readyz(request: Request):
    settings = get_settings()
    if settings.use_inmemory_store:
        return {"status": "ready", "storage": "inmemory"}
    ok = db_ping()
    if not ok:
        return JSONResponse(status_code=503, content={"status": "not_ready", "reason": "db_unreachable"})
    return {"status": "ready", "storage": "postgres"}


@app.get("/admin/metrics")
async def admin_metrics(request: Request):
    store: MetricsStore = request.app.state.metrics_store
    return {"metrics": store.snapshot()}


@app.middleware("http")
async def log_request_summary(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000.0
    http_log.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration_ms=round(duration_ms, 2),
    )
    store: MetricsStore = request.app.state.metrics_store
    store.record(request.url.path, response.status_code)
    return response


@app.middleware("http")
async def enforce_api_boundary(request: Request, call_next):
    if not request.url.path.startswith("/v1/"):
        return await call_next(request)

    settings = get_settings()
    if request_content_length_too_large(request, settings):
        return request_too_large_response()
    if not api_auth_configured(settings):
        return auth_not_configured_response()

    api_key = extract_api_key(request)
    if api_key is None:
        return missing_api_key_response()
    if not api_key_is_valid(api_key, settings):
        return invalid_api_key_response()

    request.state.api_key_fingerprint = api_key_fingerprint(api_key)
    tenant_claims, tenant_error = validate_tenant_token_for_request(request, settings)
    if tenant_error is not None:
        return tenant_error
    if tenant_claims is not None:
        request.state.tenant_claims = tenant_claims
        request.state.tenant_id = tenant_claims.tenant_id
        request.state.app_id = tenant_claims.app_id
    return await call_next(request)
