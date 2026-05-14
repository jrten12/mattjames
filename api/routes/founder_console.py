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
    .row-3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
    .row-5{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
    .row-2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
    input,select{width:100%;padding:8px;border-radius:6px;border:1px solid #4a5d71;background:#111a24;color:#eef4fb}
    textarea{width:100%;padding:8px;border-radius:6px;border:1px solid #4a5d71;background:#111a24;color:#eef4fb;min-height:90px;resize:vertical}
    button{background:#2b7fff;color:#fff;border:none;border-radius:8px;padding:8px 12px;cursor:pointer}
    button.secondary{background:#2c3e50}
    table{width:100%;border-collapse:collapse}
    th,td{padding:8px;border-bottom:1px solid #2c3e50;text-align:left;font-size:13px;vertical-align:top}
    .muted{color:#a7b8cb}
    .actions{display:flex;gap:6px;flex-wrap:wrap}
    .ok{color:#82e6b5}
    .error{color:#ff9f9f}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Founder Console</h1>
    <p class="muted">Operate intake triage, preview/approval, and release orchestration from one panel.</p>
    <div class="card">
      <h3>Quick Start</h3>
      <ol class="muted" style="margin-top:6px">
        <li>Set Base URL, API Key, and Organization ID, then refresh queue.</li>
        <li>Triage requests and assign status/priority.</li>
        <li>Create preview builds and record approval decisions.</li>
        <li>Create release records only after approved preview status.</li>
      </ol>
    </div>
    <p id="notice" class="muted"></p>

    <div class="card">
      <h3>Connection + Queue Filters</h3>
      <div class="row">
        <div><label>Base URL</label><input id="base_url" value="http://127.0.0.1:8000"/></div>
        <div><label>API Key</label><input id="api_key" placeholder="Paste your API key from setup"/></div>
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
      <h3>Preview & Approval Panel</h3>
      <p class="muted">Create preview builds, update build status, and capture approval decisions.</p>
      <div class="row-2">
        <div>
          <h4>Preview Build Manager</h4>
          <div class="row-3">
            <div><label>Intake Request ID</label><input id="preview_intake_request_id" placeholder="intake request uuid"/></div>
            <div><label>Build Version</label><input id="build_version" placeholder="v0.1.0-preview.1"/></div>
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
          <div style="margin-top:10px">
            <label>Preview URL</label>
            <input id="preview_url" placeholder="https://preview.example.com/build-1"/>
          </div>
          <div style="margin-top:10px;display:flex;gap:8px">
            <button id="createPreviewBtn">Create Preview Build</button>
            <button id="loadPreviewBtn" class="secondary">Load Preview Builds</button>
          </div>
        </div>

        <div>
          <h4>Approval Decision Manager</h4>
          <div class="row-3">
            <div><label>Intake Request ID</label><input id="approval_intake_request_id" placeholder="intake request uuid"/></div>
            <div><label>Preview Build ID</label><input id="approval_preview_build_id" placeholder="preview build uuid"/></div>
            <div><label>Decision</label>
              <select id="approval_decision">
                <option value="approve">approve</option>
                <option value="request_changes">request_changes</option>
                <option value="reject">reject</option>
              </select>
            </div>
          </div>
          <div style="margin-top:10px">
            <label>Comments</label>
            <textarea id="approval_comments" placeholder="Reasoning or requested edits"></textarea>
          </div>
          <div style="margin-top:10px;display:flex;gap:8px">
            <button id="createApprovalBtn">Create Decision</button>
            <button id="loadApprovalBtn" class="secondary">Load Decisions</button>
          </div>
        </div>
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

      <table style="margin-top:12px">
        <thead>
          <tr>
            <th>Decision ID</th>
            <th>Preview Build</th>
            <th>Decision</th>
            <th>Decided By</th>
            <th>Comments</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody id="approvalBody">
          <tr><td colspan="6" class="muted">Enter Intake Request ID to load approval decisions.</td></tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <h3>Releases Panel</h3>
      <p class="muted">Create release records from approved previews and advance release states.</p>
      <div class="row-2">
        <div>
          <h4>Create + Load Releases</h4>
          <div class="row-3">
            <div><label>Intake Request ID</label><input id="release_intake_request_id" placeholder="intake request uuid"/></div>
            <div><label>Preview Build ID</label><input id="release_preview_build_id" placeholder="preview build uuid"/></div>
            <div><label>Status Filter</label>
              <select id="release_status_filter">
                <option value="">All</option>
                <option value="pending">pending</option>
                <option value="staged">staged</option>
                <option value="approved">approved</option>
                <option value="deployed">deployed</option>
                <option value="failed">failed</option>
                <option value="rolled_back">rolled_back</option>
              </select>
            </div>
          </div>
          <div style="margin-top:10px">
            <label>Release Notes</label>
            <textarea id="release_notes" placeholder="Release context, rollout notes, or checklist"></textarea>
          </div>
          <div style="margin-top:10px;display:flex;gap:8px">
            <button id="createReleaseBtn">Create Release Record</button>
            <button id="loadReleaseBtn" class="secondary">Load Releases</button>
          </div>
        </div>

        <div>
          <h4>Advance Release Status</h4>
          <div class="row">
            <div><label>Release ID</label><input id="release_id_for_status" placeholder="release record uuid"/></div>
            <div><label>New Status</label>
              <select id="release_status_update">
                <option value="pending">pending</option>
                <option value="staged">staged</option>
                <option value="approved">approved</option>
                <option value="deployed">deployed</option>
                <option value="failed">failed</option>
                <option value="rolled_back">rolled_back</option>
              </select>
            </div>
            <div><label>Release URL</label><input id="release_url" placeholder="https://prod.example.com/app"/></div>
            <div><label>Rollback Reason</label><input id="rollback_reason" placeholder="reason when rolled_back"/></div>
          </div>
          <div style="margin-top:10px;display:flex;gap:8px">
            <button id="updateReleaseStatusBtn">Update Release Status</button>
          </div>
        </div>
      </div>

      <table style="margin-top:12px">
        <thead>
          <tr>
            <th>Release ID</th>
            <th>Status</th>
            <th>Build Version</th>
            <th>Preview Build</th>
            <th>Release URL</th>
            <th>Rollback Reason</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody id="releaseBody">
          <tr><td colspan="7" class="muted">Enter Intake Request ID to manage releases.</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <script>
    function setNotice(message, isError=false) {
      const target = document.getElementById('notice');
      target.textContent = message;
      target.className = isError ? 'error' : 'ok';
    }

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
                '<button class="secondary" onclick="openPreviewApproval(\\'' + item.id + '\\')">Open Preview/Approval</button>' +
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
      setNotice('Triage updated for intake request ' + intakeRequestId + '.');
      await refreshQueue();
    }

    async function saveStatus(intakeRequestId) {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const status = document.getElementById('status-' + intakeRequestId).value;
      if (status === 'rejected' || status === 'deployed') {
        const confirmed = window.confirm('This status is high-impact. Continue?');
        if (!confirmed) {
          setNotice('Status change cancelled.', true);
          return;
        }
      }
      await fetch(base + '/v1/intake-requests/' + intakeRequestId + '/status', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': key,
          'Idempotency-Key': 'status-' + intakeRequestId + '-' + Date.now()
        },
        body: JSON.stringify({status})
      });
      setNotice('Status updated to ' + status + ' for intake request ' + intakeRequestId + '.');
      await refreshQueue();
    }

    function openPreviewApproval(intakeRequestId) {
      document.getElementById('preview_intake_request_id').value = intakeRequestId;
      document.getElementById('approval_intake_request_id').value = intakeRequestId;
      document.getElementById('release_intake_request_id').value = intakeRequestId;
      loadPreviewBuilds();
      loadApprovalDecisions();
      loadReleaseRecords();
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
      setNotice('Preview build created for intake request ' + intakeRequestId + '.');
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
            '<td><div class="actions">' +
              '<button class="secondary" onclick="updatePreviewStatus(\\'' + item.id + '\\')">Set Status</button>' +
              '<button class="secondary" onclick="usePreviewForApproval(\\'' + item.id + '\\')">Use For Approval</button>' +
              '<button class="secondary" onclick="usePreviewForRelease(\\'' + item.id + '\\')">Use For Release</button>' +
            '</div></td>' +
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
      setNotice('Preview build ' + previewBuildId + ' moved to status "' + status + '".');
      await loadPreviewBuilds();
    }

    function usePreviewForApproval(previewBuildId) {
      document.getElementById('approval_preview_build_id').value = previewBuildId;
      setNotice('Preview build selected for approval: ' + previewBuildId + '.');
    }

    function usePreviewForRelease(previewBuildId) {
      document.getElementById('release_preview_build_id').value = previewBuildId;
      setNotice('Preview build selected for release: ' + previewBuildId + '.');
    }

    async function createApprovalDecision() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const intakeRequestId = document.getElementById('approval_intake_request_id').value.trim();
      const previewBuildId = document.getElementById('approval_preview_build_id').value.trim();
      const decision = document.getElementById('approval_decision').value;
      const commentsText = document.getElementById('approval_comments').value.trim();
      if (!intakeRequestId || !previewBuildId || !decision) {
        setNotice('Intake request ID, preview build ID, and decision are required.', true);
        return;
      }
      if (decision !== 'approve') {
        const confirmed = window.confirm('This decision can block release progression. Continue?');
        if (!confirmed) {
          setNotice('Approval decision cancelled.', true);
          return;
        }
      }
      await fetch(base + '/v1/approval-decisions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': key,
          'Idempotency-Key': 'approval-create-' + Date.now()
        },
        body: JSON.stringify({
          intake_request_id: intakeRequestId,
          preview_build_id: previewBuildId,
          decision,
          comments: commentsText || null
        })
      });
      setNotice('Approval decision "' + decision + '" recorded for intake request ' + intakeRequestId + '.');
      await loadApprovalDecisions();
      await refreshQueue();
    }

    async function loadApprovalDecisions() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const intakeRequestId = document.getElementById('approval_intake_request_id').value.trim();
      const tbody = document.getElementById('approvalBody');
      if (!intakeRequestId) {
        tbody.innerHTML = '<tr><td colspan="6" class="muted">Intake Request ID is required.</td></tr>';
        return;
      }
      try {
        const res = await fetch(
          base + '/v1/approval-decisions?intake_request_id=' + encodeURIComponent(intakeRequestId),
          {headers: {'X-API-Key': key}}
        );
        const body = await res.json();
        if (res.status < 200 || res.status >= 300 || !Array.isArray(body)) {
          tbody.innerHTML = '<tr><td colspan="6" class="muted">Failed to load approval decisions.</td></tr>';
          return;
        }
        if (body.length === 0) {
          tbody.innerHTML = '<tr><td colspan="6" class="muted">No approval decisions yet.</td></tr>';
          return;
        }
        tbody.innerHTML = body.map(item => (
          '<tr>' +
            '<td>' + item.id + '</td>' +
            '<td>' + item.preview_build_id + '</td>' +
            '<td>' + item.decision + '</td>' +
            '<td>' + (item.decided_by || 'n/a') + '</td>' +
            '<td>' + (item.comments || '') + '</td>' +
            '<td>' + item.created_at + '</td>' +
          '</tr>'
        )).join('');
      } catch (_err) {
        tbody.innerHTML = '<tr><td colspan="6" class="muted">Failed to load approval decisions.</td></tr>';
      }
    }

    async function createReleaseRecord() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const intakeRequestId = document.getElementById('release_intake_request_id').value.trim();
      const previewBuildId = document.getElementById('release_preview_build_id').value.trim();
      const notesText = document.getElementById('release_notes').value.trim();
      if (!intakeRequestId || !previewBuildId) {
        setNotice('Intake request ID and preview build ID are required for release creation.', true);
        return;
      }
      const res = await fetch(base + '/v1/releases', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': key,
          'Idempotency-Key': 'release-create-' + Date.now()
        },
        body: JSON.stringify({
          intake_request_id: intakeRequestId,
          preview_build_id: previewBuildId,
          notes: notesText || null
        })
      });
      if (res.status < 200 || res.status >= 300) {
        setNotice('Failed to create release record. Ensure preview is ready and latest decision is approve.', true);
        return;
      }
      setNotice('Release record created for intake request ' + intakeRequestId + '.');
      await loadReleaseRecords();
    }

    async function loadReleaseRecords() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const intakeRequestId = document.getElementById('release_intake_request_id').value.trim();
      const statusFilter = document.getElementById('release_status_filter').value;
      const tbody = document.getElementById('releaseBody');
      if (!intakeRequestId) {
        tbody.innerHTML = '<tr><td colspan="7" class="muted">Intake Request ID is required.</td></tr>';
        return;
      }
      const params = new URLSearchParams({intake_request_id: intakeRequestId});
      if (statusFilter) params.set('status', statusFilter);
      try {
        const res = await fetch(base + '/v1/releases?' + params.toString(), {headers: {'X-API-Key': key}});
        const body = await res.json();
        if (res.status < 200 || res.status >= 300 || !Array.isArray(body)) {
          tbody.innerHTML = '<tr><td colspan="7" class="muted">Failed to load release records.</td></tr>';
          return;
        }
        if (body.length === 0) {
          tbody.innerHTML = '<tr><td colspan="7" class="muted">No releases yet.</td></tr>';
          return;
        }
        tbody.innerHTML = body.map(item => (
          '<tr>' +
            '<td>' + item.id + '</td>' +
            '<td>' + item.status + '</td>' +
            '<td>' + item.build_version + '</td>' +
            '<td>' + item.preview_build_id + '</td>' +
            '<td>' + (item.release_url || '') + '</td>' +
            '<td>' + (item.rollback_reason || '') + '</td>' +
            '<td><button class="secondary" onclick="useReleaseForStatus(\\'' + item.id + '\\')">Set Active Release</button></td>' +
          '</tr>'
        )).join('');
      } catch (_err) {
        tbody.innerHTML = '<tr><td colspan="7" class="muted">Failed to load release records.</td></tr>';
      }
    }

    function useReleaseForStatus(releaseId) {
      document.getElementById('release_id_for_status').value = releaseId;
      setNotice('Release selected for status update: ' + releaseId + '.');
    }

    async function updateReleaseRecordStatus() {
      const base = document.getElementById('base_url').value.trim();
      const key = document.getElementById('api_key').value.trim();
      const releaseId = document.getElementById('release_id_for_status').value.trim();
      const status = document.getElementById('release_status_update').value;
      const releaseUrl = document.getElementById('release_url').value.trim();
      const rollbackReason = document.getElementById('rollback_reason').value.trim();
      const notesText = document.getElementById('release_notes').value.trim();
      if (!releaseId) {
        setNotice('Release ID is required to update release status.', true);
        return;
      }
      if (status === 'failed' || status === 'rolled_back') {
        const confirmed = window.confirm('This marks a failed or rolled-back release. Continue?');
        if (!confirmed) {
          setNotice('Release update cancelled.', true);
          return;
        }
      }
      const res = await fetch(base + '/v1/releases/' + releaseId + '/status', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': key,
          'Idempotency-Key': 'release-status-' + releaseId + '-' + Date.now()
        },
        body: JSON.stringify({
          status,
          release_url: releaseUrl || null,
          rollback_reason: rollbackReason || null,
          notes: notesText || null
        })
      });
      if (res.status < 200 || res.status >= 300) {
        setNotice('Failed to update release status.', true);
        return;
      }
      setNotice('Release ' + releaseId + ' moved to status "' + status + '".');
      await loadReleaseRecords();
      await refreshQueue();
    }

    document.getElementById('createPreviewBtn').addEventListener('click', createPreviewBuild);
    document.getElementById('loadPreviewBtn').addEventListener('click', loadPreviewBuilds);
    document.getElementById('createApprovalBtn').addEventListener('click', createApprovalDecision);
    document.getElementById('loadApprovalBtn').addEventListener('click', loadApprovalDecisions);
    document.getElementById('createReleaseBtn').addEventListener('click', createReleaseRecord);
    document.getElementById('loadReleaseBtn').addEventListener('click', loadReleaseRecords);
    document.getElementById('updateReleaseStatusBtn').addEventListener('click', updateReleaseRecordStatus);
  </script>
</body>
</html>
"""
