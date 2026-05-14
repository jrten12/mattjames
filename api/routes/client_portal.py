from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/portal", response_class=HTMLResponse)
async def client_portal_shell() -> str:
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Matt James Client Portal</title>
  <style>
    :root{
      --bg:#081123;
      --bg-soft:#0d1b33;
      --panel:#101d35;
      --panel-2:#132443;
      --text:#ecf2ff;
      --muted:#9bb0d6;
      --line:#263d66;
      --accent:#4f8cff;
      --accent-2:#7c5dff;
      --ok:#5ad4a8;
      --warn:#ffc266;
      --error:#ff8a8a;
    }
    *{box-sizing:border-box}
    body{
      font-family:Inter,Segoe UI,Arial,sans-serif;
      margin:0;
      color:var(--text);
      background:
        radial-gradient(circle at 20% 0%, rgba(79,140,255,.28), transparent 38%),
        radial-gradient(circle at 80% -10%, rgba(124,93,255,.22), transparent 35%),
        var(--bg);
    }
    .wrap{max-width:1160px;margin:0 auto;padding:28px 20px 40px}
    .hero{
      display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;
      margin-bottom:14px
    }
    .title{margin:0;font-size:30px;letter-spacing:.2px}
    .subtitle{margin:6px 0 0;color:var(--muted)}
    .pill{
      border:1px solid var(--line);
      background:rgba(16,29,53,.75);
      color:var(--muted);
      border-radius:999px;
      padding:8px 12px;
      font-size:12px;
    }
    .grid{display:grid;grid-template-columns:2fr 1fr;gap:14px}
    .card{
      background:linear-gradient(180deg,rgba(19,36,67,.9),rgba(16,29,53,.96));
      border:1px solid var(--line);
      border-radius:14px;
      padding:16px;
      box-shadow:0 10px 30px rgba(0,0,0,.22);
    }
    .card h3{margin:0 0 10px 0;font-size:18px}
    .card h4{margin:0 0 8px 0;font-size:14px;color:#d7e3ff}
    .muted{color:var(--muted)}
    .small{font-size:12px}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    .row-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
    label{font-size:12px;color:var(--muted);display:block;margin-bottom:5px}
    input,select,textarea{
      width:100%;
      border-radius:10px;
      border:1px solid #36517f;
      background:#0b162a;
      color:var(--text);
      padding:10px 11px;
      outline:none;
    }
    input:focus,select:focus,textarea:focus{border-color:var(--accent)}
    textarea{min-height:110px;resize:vertical}
    button{
      border:none;
      border-radius:10px;
      padding:10px 14px;
      cursor:pointer;
      color:white;
      background:linear-gradient(90deg,var(--accent),var(--accent-2));
      font-weight:600;
    }
    button.secondary{background:#243d68;color:#d3e2ff}
    button:disabled{opacity:.5;cursor:not-allowed}
    .list{margin:0;padding-left:18px;color:var(--muted)}
    .list li{margin:4px 0}
    .steps{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;margin:8px 0 14px}
    .step{
      padding:8px 10px;
      border-radius:10px;
      background:#10203c;
      color:#9eb4dd;
      border:1px solid #2f4a75;
      font-size:12px;
      text-align:center;
      font-weight:600;
    }
    .step.active{background:#1e3f74;color:white;border-color:#5f91eb}
    .actions{display:flex;justify-content:space-between;margin-top:12px}
    .hidden{display:none}
    pre{
      background:#091427;
      border:1px solid #2a446f;
      border-radius:10px;
      padding:12px;
      overflow:auto;
      margin:0;
      white-space:pre-wrap;
    }
    table{width:100%;border-collapse:collapse}
    th,td{
      padding:10px 8px;
      border-bottom:1px solid #2d4670;
      text-align:left;
      font-size:13px;
      vertical-align:top;
    }
    th{color:#bad0f5;font-size:12px;letter-spacing:.2px}
    .status{
      display:inline-block;
      font-size:11px;
      border:1px solid #3a5f94;
      color:#bdd2f5;
      border-radius:999px;
      padding:4px 8px;
      text-transform:capitalize;
    }
    .quick{display:flex;gap:8px;flex-wrap:wrap}
    .quick .item{
      flex:1 1 170px;
      background:#0c1a31;
      border:1px solid #2b446e;
      border-radius:10px;
      padding:10px;
      font-size:12px;
      color:var(--muted);
    }
    .toolbar{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
    .link{color:#a9c8ff;text-decoration:none}
    .alert{margin:0 0 12px 0;padding:10px;border-radius:10px;border:1px solid #345486;background:#10233f;color:#c2d8ff}
    @media (max-width:960px){
      .grid{grid-template-columns:1fr}
      .steps{grid-template-columns:repeat(3,minmax(0,1fr))}
      .row,.row-3{grid-template-columns:1fr}
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="hero">
      <div>
        <h1 class="title">Client Portal</h1>
        <p class="subtitle">Simple request intake, preview review, and approval in one clean workspace.</p>
      </div>
      <div class="pill">Designed for non-technical users</div>
    </div>

    <div class="grid">
      <div class="card">
        <h3>How this works</h3>
        <ol class="list small">
        <li>Fill in Base URL, API Key, and Organization ID.</li>
        <li>Use the guided request wizard (left panel).</li>
        <li>Track live status in My Requests.</li>
        <li>Open preview and submit decision when ready.</li>
      </ol>
        <div class="quick" style="margin-top:12px">
          <div class="item"><strong>Default flow</strong><br/>Submit request -> review preview -> approve or request changes.</div>
          <div class="item"><strong>You should never need IDs</strong><br/>Pick requests from dropdowns once loaded.</div>
          <div class="item"><strong>Safe actions</strong><br/>High-impact decisions ask for confirmation.</div>
        </div>
      </div>

      <div class="card">
        <h3>Workspace setup</h3>
        <div class="row">
          <div><label>Base URL</label><input id="base_url" value="http://127.0.0.1:8000"/></div>
          <div><label>API Key</label><input id="api_key" placeholder="Paste your API key from setup"/></div>
          <div><label>Organization ID</label><input id="organization_id" placeholder="Organization UUID"/></div>
          <div><label>Project ID (optional)</label><input id="project_id" placeholder="Project UUID (optional)"/></div>
        </div>
      </div>

      <div class="card">
        <h3>New Request</h3>
        <div class="alert small">The portal turns your answers into a clean API request automatically.</div>
        <div class="steps">
          <div id="indicator-0" class="step active">1. Type</div>
          <div id="indicator-1" class="step">2. Goal</div>
          <div id="indicator-2" class="step">3. Features</div>
          <div id="indicator-3" class="step">4. Assets</div>
          <div id="indicator-4" class="step">5. Success</div>
          <div id="indicator-5" class="step">6. Submit</div>
        </div>

        <div id="step-0">
          <div class="row">
            <div>
              <label>Request Type</label>
              <select id="request_type">
                <option value="new_app">New app</option>
                <option value="update">Update</option>
                <option value="bugfix">Bugfix</option>
                <option value="enhancement">Enhancement</option>
              </select>
            </div>
            <div>
              <label>Request Title</label>
              <input id="title" placeholder="Example: Improve onboarding flow"/>
            </div>
          </div>
        </div>

        <div id="step-1" class="hidden">
          <label>Business Goal</label>
          <textarea id="goal" placeholder="What outcome should this request achieve?"></textarea>
        </div>

        <div id="step-2" class="hidden">
          <label>Required Features</label>
          <textarea id="features" placeholder="List requested features in plain language."></textarea>
        </div>

        <div id="step-3" class="hidden">
          <label>Assets and References</label>
          <textarea id="assets" placeholder="Optional links, docs, examples, screenshots, or process notes."></textarea>
        </div>

        <div id="step-4" class="hidden">
          <label>Success Criteria</label>
          <textarea id="success" placeholder="How should success be measured?"></textarea>
        </div>

        <div id="step-5" class="hidden">
          <p class="muted small">Review before submission:</p>
          <pre id="review"></pre>
        </div>

        <div class="actions">
          <button id="backBtn" class="secondary">Back</button>
          <button id="nextBtn">Next Step</button>
        </div>
      </div>

      <div class="card">
        <h3>Result</h3>
        <pre id="result">{ "status": "idle" }</pre>
      </div>
      </div>

      <div style="display:grid;gap:14px">
        <div class="card">
          <div class="toolbar">
            <h3 style="margin:0">My Requests</h3>
            <button id="refreshBtn" class="secondary">Refresh</button>
          </div>
          <table style="margin-top:10px">
            <thead>
              <tr>
                <th>Title</th>
                <th>Type</th>
                <th>Status</th>
                <th>Updated</th>
              </tr>
            </thead>
            <tbody id="requestsBody">
              <tr><td colspan="4" class="muted">No requests yet.</td></tr>
            </tbody>
          </table>
        </div>

        <div class="card">
          <h3>Preview Review</h3>
          <div class="row">
            <div>
              <label>Select Request</label>
              <select id="preview_request_select">
                <option value="">Select a request...</option>
              </select>
            </div>
            <div>
              <label>Decision</label>
              <select id="preview_decision">
                <option value="approve">Approve</option>
                <option value="request_changes">Request Changes</option>
                <option value="reject">Reject</option>
              </select>
            </div>
          </div>
          <div style="margin-top:10px;display:flex;gap:8px;align-items:center">
            <button id="loadPreviewBtn" class="secondary">Load Preview</button>
            <a id="openPreviewLink" href="#" target="_blank" class="link" style="display:none">Open Preview</a>
          </div>
          <div style="margin-top:10px">
            <label>Feedback</label>
            <textarea id="preview_feedback" placeholder="Share what works well and what should change."></textarea>
          </div>
          <div style="margin-top:10px">
            <button id="submitDecisionBtn">Submit Decision</button>
          </select>
        </div>
          <p class="muted small" style="margin:8px 0 0">Non-approve decisions ask for confirmation because they can delay release.</p>
          <pre id="previewMeta" style="margin-top:10px">{ "status": "idle" }</pre>
        </div>
      </div>
    </div>
  </div>

  <script>
    const steps = [0,1,2,3,4,5];
    let stepIndex = 0;
    let cachedRequests = [];
    let selectedPreviewBuild = null;

    function requestPayload() {
      const features = document.getElementById('features').value.trim();
      const assets = document.getElementById('assets').value.trim();
      const success = document.getElementById('success').value.trim();
      const detailsParts = [];
      if (features) detailsParts.push('Required features:\\n' + features);
      if (assets) detailsParts.push('Assets and references:\\n' + assets);
      if (success) detailsParts.push('Success criteria:\\n' + success);
      const payload = {
        organization_id: document.getElementById('organization_id').value.trim(),
        request_type: document.getElementById('request_type').value,
        title: document.getElementById('title').value.trim(),
        goal: document.getElementById('goal').value.trim(),
        details: detailsParts.join('\\n\\n') || null
      };
      const projectId = document.getElementById('project_id').value.trim();
      if (projectId) payload.project_id = projectId;
      return payload;
    }

    function updateStepUi() {
      for (const idx of steps) {
        document.getElementById('step-' + idx).classList.toggle('hidden', idx !== stepIndex);
        document.getElementById('indicator-' + idx).classList.toggle('active', idx === stepIndex);
      }
      document.getElementById('backBtn').disabled = stepIndex === 0;
      document.getElementById('nextBtn').textContent = stepIndex === 5 ? 'Submit Request' : 'Next';
      if (stepIndex === 5) {
        document.getElementById('review').textContent = JSON.stringify(requestPayload(), null, 2);
      }
    }

    async function submitRequest() {
      const payload = requestPayload();
      const out = document.getElementById('result');
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      if (!payload.organization_id || !payload.title || !payload.goal) {
        out.textContent = JSON.stringify(
          {status: 'error', message: 'Organization ID, title, and goal are required.'},
          null,
          2
        );
        return;
      }
      out.textContent = '{ "status": "working" }';
      const confirmed = window.confirm('Submit this request now?');
      if (!confirmed) {
        out.textContent = JSON.stringify({status: 'cancelled', message: 'Submission cancelled by user.'}, null, 2);
        return;
      }
      try {
        const res = await fetch(base + '/v1/intake-requests', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': key,
            'Idempotency-Key': 'client-req-' + Date.now()
          },
          body: JSON.stringify(payload)
        });
        const body = await res.json();
        out.textContent = JSON.stringify({status: res.status, body}, null, 2);
        if (res.status >= 200 && res.status < 300) {
          stepIndex = 0;
          updateStepUi();
          await refreshRequests();
        }
      } catch (err) {
        out.textContent = JSON.stringify({status: 'error', message: String(err)}, null, 2);
      }
    }

    async function refreshRequests() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const orgId = document.getElementById('organization_id').value.trim();
      const tbody = document.getElementById('requestsBody');
      const requestSelect = document.getElementById('preview_request_select');
      if (!orgId) {
        tbody.innerHTML = '<tr><td colspan="4" class="muted">Set Organization ID to load requests.</td></tr>';
        requestSelect.innerHTML = '<option value="">Select a request...</option>';
        cachedRequests = [];
        return;
      }
      try {
        const res = await fetch(base + '/v1/intake-requests?organization_id=' + encodeURIComponent(orgId), {
          headers: {'X-API-Key': key}
        });
        const body = await res.json();
        if (res.status < 200 || res.status >= 300) {
          tbody.innerHTML = '<tr><td colspan="4" class="muted">Failed to load requests.</td></tr>';
          requestSelect.innerHTML = '<option value="">Select a request...</option>';
          cachedRequests = [];
          return;
        }
        if (!Array.isArray(body) || body.length === 0) {
          tbody.innerHTML = '<tr><td colspan="4" class="muted">No requests yet.</td></tr>';
          requestSelect.innerHTML = '<option value="">Select a request...</option>';
          cachedRequests = [];
          return;
        }
        cachedRequests = body;
        requestSelect.innerHTML =
          '<option value="">Select a request...</option>' +
          body.map(item => (
            '<option value="' + item.id + '">' + item.title + ' (' + item.status + ')</option>'
          )).join('');
        tbody.innerHTML = body.map(item => (
          '<tr>' +
            '<td>' + item.title + '</td>' +
            '<td>' + item.request_type + '</td>' +
            '<td><span class="status">' + item.status.replaceAll('_', ' ') + '</span></td>' +
            '<td>' + item.updated_at + '</td>' +
          '</tr>'
        )).join('');
      } catch (_err) {
        tbody.innerHTML = '<tr><td colspan="4" class="muted">Failed to load requests.</td></tr>';
        requestSelect.innerHTML = '<option value="">Select a request...</option>';
        cachedRequests = [];
      }
    }

    function decisionToStatus(decision) {
      if (decision === 'approve') return 'approved';
      if (decision === 'request_changes') return 'changes_requested';
      return 'rejected';
    }

    async function loadPreviewForSelectedRequest() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const intakeRequestId = document.getElementById('preview_request_select').value;
      const meta = document.getElementById('previewMeta');
      const openLink = document.getElementById('openPreviewLink');
      selectedPreviewBuild = null;
      openLink.style.display = 'none';
      if (!intakeRequestId) {
        meta.textContent = JSON.stringify({status: 'error', message: 'Select a request first.'}, null, 2);
        return;
      }
      try {
        const res = await fetch(
          base + '/v1/preview-builds?intake_request_id=' + encodeURIComponent(intakeRequestId),
          {headers: {'X-API-Key': key}}
        );
        const body = await res.json();
        if (res.status < 200 || res.status >= 300 || !Array.isArray(body) || body.length === 0) {
          meta.textContent = JSON.stringify(
            {status: 'empty', message: 'No preview build found for this request yet.'},
            null,
            2
          );
          return;
        }
        selectedPreviewBuild = body[0];
        openLink.href = selectedPreviewBuild.preview_url;
        openLink.style.display = 'inline';
        meta.textContent = JSON.stringify(
          {
            status: 'ok',
            build_id: selectedPreviewBuild.id,
            build_version: selectedPreviewBuild.build_version,
            preview_url: selectedPreviewBuild.preview_url,
            preview_status: selectedPreviewBuild.status,
          },
          null,
          2
        );
      } catch (err) {
        meta.textContent = JSON.stringify({status: 'error', message: String(err)}, null, 2);
      }
    }

    async function submitPreviewDecision() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const intakeRequestId = document.getElementById('preview_request_select').value;
      const decision = document.getElementById('preview_decision').value;
      const feedback = document.getElementById('preview_feedback').value.trim();
      const meta = document.getElementById('previewMeta');
      if (!intakeRequestId) {
        meta.textContent = JSON.stringify({status: 'error', message: 'Select a request first.'}, null, 2);
        return;
      }
      const nextStatus = decisionToStatus(decision);
      if (decision !== 'approve') {
        const confirmed = window.confirm('This decision may delay release progress. Continue?');
        if (!confirmed) {
          meta.textContent = JSON.stringify({status: 'cancelled', message: 'Decision cancelled by user.'}, null, 2);
          return;
        }
      }
      try {
        const res = await fetch(base + '/v1/intake-requests/' + intakeRequestId + '/status', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': key,
            'Idempotency-Key': 'client-decision-' + intakeRequestId + '-' + Date.now()
          },
          body: JSON.stringify({status: nextStatus})
        });
        const body = await res.json();
        meta.textContent = JSON.stringify(
          {
            status: res.status,
            decision,
            mapped_status: nextStatus,
            feedback,
            body
          },
          null,
          2
        );
        await refreshRequests();
      } catch (err) {
        meta.textContent = JSON.stringify({status: 'error', message: String(err)}, null, 2);
      }
    }

    document.getElementById('backBtn').addEventListener('click', () => {
      if (stepIndex > 0) {
        stepIndex -= 1;
        updateStepUi();
      }
    });
    document.getElementById('nextBtn').addEventListener('click', async () => {
      if (stepIndex < 5) {
        stepIndex += 1;
        updateStepUi();
        return;
      }
      await submitRequest();
    });
    document.getElementById('refreshBtn').addEventListener('click', refreshRequests);
    document.getElementById('loadPreviewBtn').addEventListener('click', loadPreviewForSelectedRequest);
    document.getElementById('submitDecisionBtn').addEventListener('click', submitPreviewDecision);
    updateStepUi();
  </script>
</body>
</html>
"""
