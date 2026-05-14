from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/founder", response_class=HTMLResponse)
async def founder_console_shell() -> str:
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Matt James Founder Console</title>
  <style>
    body{font-family:Arial,sans-serif;margin:0;background:#0f1720;color:#e8edf5}
    .wrap{max-width:1200px;margin:0 auto;padding:24px}
    .card{background:#1b2633;border:1px solid #2c3e50;border-radius:10px;padding:16px;margin-top:16px}
    .row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}
    input,select{width:100%;padding:8px;border-radius:6px;border:1px solid #4a5d71;background:#111a24;color:#eef4fb}
    button{background:#2b7fff;color:#fff;border:none;border-radius:8px;padding:8px 12px;cursor:pointer}
    button.secondary{background:#2c3e50}
    table{width:100%;border-collapse:collapse}
    th,td{padding:8px;border-bottom:1px solid #2c3e50;text-align:left;font-size:13px;vertical-align:top}
    .muted{color:#a7b8cb}
    .actions{display:flex;gap:6px;flex-wrap:wrap}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Founder Console - Intake Queue</h1>
    <p class="muted">Triage incoming client requests, assign owner, set priority, and move status.</p>

    <div class="card">
      <h3>Connection + Filters</h3>
      <div class="row">
        <div><label>Base URL</label><input id="base_url" value="http://127.0.0.1:8000"/></div>
        <div><label>API Key</label><input id="api_key" placeholder="paste PLATFORM_API_KEYS value"/></div>
        <div><label>Organization ID</label><input id="organization_id" placeholder="org uuid"/></div>
        <div><label>Status Filter</label>
          <select id="status_filter">
            <option value="">All</option>
            <option value="submitted">submitted</option>
            <option value="triaged">triaged</option>
            <option value="building">building</option>
            <option value="preview_ready">preview_ready</option>
            <option value="client_review">client_review</option>
            <option value="changes_requested">changes_requested</option>
            <option value="approved">approved</option>
            <option value="deployed">deployed</option>
            <option value="rejected">rejected</option>
          </select>
        </div>
      </div>
      <div style="margin-top:10px;display:flex;gap:8px">
        <button id="refreshBtn">Refresh Queue</button>
      </div>
    </div>

    <div class="card">
      <h3>Intake Queue</h3>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Type</th>
            <th>Status</th>
            <th>Owner</th>
            <th>Priority</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="queueBody">
          <tr><td colspan="6" class="muted">Set Organization ID then click Refresh Queue.</td></tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h3>Preview Builds</h3>
      <div class="row">
        <div><label>Intake Request ID</label><input id="preview_intake_request_id" placeholder="intake request uuid"/></div>
        <div><label>Build Version</label><input id="build_version" placeholder="v0.1.0-preview.1"/></div>
        <div><label>Preview URL</label><input id="preview_url" placeholder="https://preview.example.com/build-1"/></div>
        <div><label>Status (for update)</label>
          <select id="preview_status">
            <option value="queued">queued</option>
            <option value="building">building</option>
            <option value="ready">ready</option>
            <option value="failed">failed</option>
            <option value="expired">expired</option>
          </select>
        </div>
      </div>
      <div style="margin-top:10px;display:flex;gap:8px">
        <button id="createPreviewBtn">Create Preview Build</button>
        <button id="loadPreviewBtn" class="secondary">Load Preview Builds</button>
      </div>
      <table style="margin-top:12px">
        <thead>
          <tr>
            <th>Build ID</th>
            <th>Version</th>
            <th>Status</th>
            <th>Preview URL</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody id="previewBody">
          <tr><td colspan="5" class="muted">Enter Intake Request ID to manage preview builds.</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <script>
    async function refreshQueue() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const orgId = document.getElementById('organization_id').value.trim();
      const status = document.getElementById('status_filter').value;
      const tbody = document.getElementById('queueBody');
      if (!orgId) {
        tbody.innerHTML = '<tr><td colspan="6" class="muted">Organization ID is required.</td></tr>';
        return;
      }
      const params = new URLSearchParams({organization_id: orgId});
      if (status) params.set('status', status);
      try {
        const res = await fetch(base + '/v1/intake-requests?' + params.toString(), {
          headers: {'X-API-Key': key}
        });
        const body = await res.json();
        if (res.status < 200 || res.status >= 300 || !Array.isArray(body)) {
          tbody.innerHTML = '<tr><td colspan="6" class="muted">Failed to load queue.</td></tr>';
          return;
        }
        if (body.length === 0) {
          tbody.innerHTML = '<tr><td colspan="6" class="muted">No intake requests found.</td></tr>';
          return;
        }
        tbody.innerHTML = body.map(item => {
          const owner = item.owner_user_id || '';
          const priority = item.priority || 'normal';
          return (
            '<tr>' +
              '<td><strong>' + item.title + '</strong><br/><span class="muted">' + (item.goal || '') + '</span></td>' +
              '<td>' + item.request_type + '</td>' +
              '<td><select id="status-' + item.id + '">' +
                statusOptions(item.status) +
              '</select></td>' +
              '<td><input id="owner-' + item.id + '" value="' + owner + '" placeholder="owner_user_id"/></td>' +
              '<td><select id="priority-' + item.id + '">' +
                priorityOptions(priority) +
              '</select></td>' +
              '<td><div class="actions">' +
                '<button onclick="saveTriage(\\'' + item.id + '\\')">Save Triage</button>' +
                '<button class="secondary" onclick="saveStatus(\\'' + item.id + '\\')">Update Status</button>' +
              '</div></td>' +
            '</tr>'
          );
        }).join('');
      } catch (_err) {
        tbody.innerHTML = '<tr><td colspan="6" class="muted">Failed to load queue.</td></tr>';
      }
    }

    function statusOptions(current) {
      const options = [
        'submitted','triaged','building','preview_ready','client_review',
        'changes_requested','approved','deployed','rejected'
      ];
      return options.map(value =>
        '<option value="' + value + '"' + (value === current ? ' selected' : '') + '>' + value + '</option>'
      ).join('');
    }

    function priorityOptions(current) {
      const options = ['low','normal','high','urgent'];
      return options.map(value =>
        '<option value="' + value + '"' + (value === current ? ' selected' : '') + '>' + value + '</option>'
      ).join('');
    }

    async function saveTriage(intakeRequestId) {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const owner = document.getElementById('owner-' + intakeRequestId).value.trim();
      const priority = document.getElementById('priority-' + intakeRequestId).value;
      await fetch(base + '/v1/intake-requests/' + intakeRequestId + '/triage', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': key,
          'Idempotency-Key': 'triage-' + intakeRequestId + '-' + Date.now()
        },
        body: JSON.stringify({
          owner_user_id: owner || null,
          priority
        })
      });
      await refreshQueue();
    }

    async function saveStatus(intakeRequestId) {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const status = document.getElementById('status-' + intakeRequestId).value;
      await fetch(base + '/v1/intake-requests/' + intakeRequestId + '/status', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': key,
          'Idempotency-Key': 'status-' + intakeRequestId + '-' + Date.now()
        },
        body: JSON.stringify({status})
      });
      await refreshQueue();
    }

    document.getElementById('refreshBtn').addEventListener('click', refreshQueue);

    async function createPreviewBuild() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const intakeRequestId = document.getElementById('preview_intake_request_id').value.trim();
      const buildVersion = document.getElementById('build_version').value.trim();
      const previewUrl = document.getElementById('preview_url').value.trim();
      if (!intakeRequestId || !buildVersion || !previewUrl) {
        return;
      }
      await fetch(base + '/v1/preview-builds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': key,
          'Idempotency-Key': 'preview-create-' + Date.now()
        },
        body: JSON.stringify({
          intake_request_id: intakeRequestId,
          build_version: buildVersion,
          preview_url: previewUrl
        })
      });
      await loadPreviewBuilds();
    }

    async function loadPreviewBuilds() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const intakeRequestId = document.getElementById('preview_intake_request_id').value.trim();
      const tbody = document.getElementById('previewBody');
      if (!intakeRequestId) {
        tbody.innerHTML = '<tr><td colspan="5" class="muted">Intake Request ID is required.</td></tr>';
        return;
      }
      try {
        const res = await fetch(
          base + '/v1/preview-builds?intake_request_id=' + encodeURIComponent(intakeRequestId),
          {headers: {'X-API-Key': key}}
        );
        const body = await res.json();
        if (res.status < 200 || res.status >= 300 || !Array.isArray(body)) {
          tbody.innerHTML = '<tr><td colspan="5" class="muted">Failed to load preview builds.</td></tr>';
          return;
        }
        if (body.length === 0) {
          tbody.innerHTML = '<tr><td colspan="5" class="muted">No preview builds yet.</td></tr>';
          return;
        }
        tbody.innerHTML = body.map(item => (
          '<tr>' +
            '<td>' + item.id + '</td>' +
            '<td>' + item.build_version + '</td>' +
            '<td>' + item.status + '</td>' +
            '<td><a href="' + item.preview_url + '" target="_blank" style="color:#9ecbff">open</a></td>' +
            '<td><button class="secondary" onclick="updatePreviewStatus(\\'' + item.id + '\\')">Set Status</button></td>' +
          '</tr>'
        )).join('');
      } catch (_err) {
        tbody.innerHTML = '<tr><td colspan="5" class="muted">Failed to load preview builds.</td></tr>';
      }
    }

    async function updatePreviewStatus(previewBuildId) {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const status = document.getElementById('preview_status').value;
      await fetch(base + '/v1/preview-builds/' + previewBuildId + '/status', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': key,
          'Idempotency-Key': 'preview-status-' + previewBuildId + '-' + Date.now()
        },
        body: JSON.stringify({status})
      });
      await loadPreviewBuilds();
    }

    document.getElementById('createPreviewBtn').addEventListener('click', createPreviewBuild);
    document.getElementById('loadPreviewBtn').addEventListener('click', loadPreviewBuilds);
  </script>
</body>
</html>
"""
