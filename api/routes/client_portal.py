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
    body{font-family:Arial,sans-serif;margin:0;background:#0f1720;color:#e8edf5}
    .wrap{max-width:1100px;margin:0 auto;padding:24px}
    .card{background:#1b2633;border:1px solid #2c3e50;border-radius:10px;padding:16px;margin-top:16px}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:10px}
    .steps{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 14px 0}
    .step{padding:6px 10px;border-radius:999px;background:#243447;color:#a7b8cb;border:1px solid #38516a}
    .step.active{background:#2b7fff;color:#fff;border-color:#2b7fff}
    button{background:#2b7fff;color:#fff;border:none;border-radius:8px;padding:10px 14px;cursor:pointer}
    button.secondary{background:#2c3e50}
    input,select,textarea{width:100%;padding:8px;border-radius:6px;border:1px solid #4a5d71;background:#111a24;color:#eef4fb}
    textarea{min-height:110px;resize:vertical}
    label{font-size:12px;color:#a7b8cb}
    .actions{display:flex;justify-content:space-between;margin-top:12px}
    .hidden{display:none}
    .muted{color:#a7b8cb}
    pre{background:#0d141d;border:1px solid #243344;border-radius:8px;padding:12px;overflow:auto}
    table{width:100%;border-collapse:collapse}
    th,td{padding:8px;border-bottom:1px solid #2c3e50;text-align:left;font-size:13px}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Client Portal</h1>
    <p class="muted">Submit a new request, then track status in one place.</p>

    <div class="card">
      <h3>Connection</h3>
      <div class="row">
        <div><label>Base URL</label><input id="base_url" value="http://127.0.0.1:8000"/></div>
        <div><label>API Key</label><input id="api_key" placeholder="paste PLATFORM_API_KEYS value"/></div>
        <div><label>Organization ID</label><input id="organization_id" placeholder="org uuid"/></div>
        <div><label>Project ID (optional)</label><input id="project_id" placeholder="project uuid"/></div>
      </div>
    </div>

    <div class="card">
      <h3>New Request</h3>
      <div class="steps">
        <div id="indicator-0" class="step active">1. Type</div>
        <div id="indicator-1" class="step">2. Goal</div>
        <div id="indicator-2" class="step">3. Features</div>
        <div id="indicator-3" class="step">4. Assets</div>
        <div id="indicator-4" class="step">5. Success</div>
        <div id="indicator-5" class="step">6. Submit</div>
      </div>

      <div id="step-0">
        <label>Request Type</label>
        <select id="request_type">
          <option value="new_app">New app</option>
          <option value="update">Update</option>
          <option value="bugfix">Bugfix</option>
          <option value="enhancement">Enhancement</option>
        </select>
        <label style="margin-top:8px;display:block">Request Title</label>
        <input id="title" placeholder="Example: Intake wizard and review flow"/>
      </div>

      <div id="step-1" class="hidden">
        <label>Business Goal</label>
        <textarea id="goal" placeholder="What outcome do you want from this request?"></textarea>
      </div>

      <div id="step-2" class="hidden">
        <label>Required Features</label>
        <textarea id="features" placeholder="List required features in plain language."></textarea>
      </div>

      <div id="step-3" class="hidden">
        <label>Assets and References</label>
        <textarea id="assets" placeholder="Links, docs, screenshots, process notes."></textarea>
      </div>

      <div id="step-4" class="hidden">
        <label>Success Criteria</label>
        <textarea id="success" placeholder="How should we measure success?"></textarea>
      </div>

      <div id="step-5" class="hidden">
        <p class="muted">Review before submission.</p>
        <pre id="review"></pre>
      </div>

      <div class="actions">
        <button id="backBtn" class="secondary">Back</button>
        <button id="nextBtn">Next</button>
      </div>
    </div>

    <div class="card">
      <h3>Result</h3>
      <pre id="result">{ "status": "idle" }</pre>
    </div>

    <div class="card">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <h3 style="margin:0">My Requests</h3>
        <button id="refreshBtn" class="secondary">Refresh</button>
      </div>
      <table>
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
      <div style="margin-top:10px;display:flex;gap:8px">
        <button id="loadPreviewBtn" class="secondary">Load Preview</button>
        <a id="openPreviewLink" href="#" target="_blank" style="display:none;color:#9ecbff;padding-top:10px">Open Preview</a>
      </div>
      <div style="margin-top:10px">
        <label>Feedback</label>
        <textarea id="preview_feedback" placeholder="Share what works, what should change, and why."></textarea>
      </div>
      <div style="margin-top:10px">
        <button id="submitDecisionBtn">Submit Decision</button>
      </div>
      <pre id="previewMeta" style="margin-top:10px">{ "status": "idle" }</pre>
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
            '<td>' + item.status + '</td>' +
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
