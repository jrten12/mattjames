def render_client_portal_html() -> str:
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Matt James Intake Portal</title>
  <style>
    :root {
      --page-bg: #f7f5f2;
      --surface: #ffffff;
      --surface-soft: #fcfaf7;
      --line: #e6dfd5;
      --line-strong: #d8cebf;
      --text: #2b2a28;
      --text-muted: #6e6860;
      --brand: #5a49d6;
      --brand-strong: #4738be;
      --success: #206a3d;
      --success-bg: #e6f4ea;
      --warning: #946a04;
      --warning-bg: #fff7e5;
      --shadow: 0 10px 25px rgba(21, 15, 6, 0.08);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: "Inter", "Segoe UI", Arial, sans-serif;
      color: var(--text);
      background: linear-gradient(180deg, #fdfcfb 0%, var(--page-bg) 120%);
      line-height: 1.5;
    }
    .top-nav {
      position: sticky;
      top: 0;
      z-index: 5;
      background: rgba(253, 252, 251, 0.95);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--line);
    }
    .top-nav-inner {
      max-width: 1200px;
      margin: 0 auto;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 700;
      letter-spacing: 0.2px;
    }
    .brand-mark {
      width: 30px;
      height: 30px;
      border-radius: 10px;
      background: linear-gradient(135deg, #7967ea, #4f3fd0);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 13px;
      font-weight: 800;
    }
    .nav-links {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .nav-links button {
      border: 1px solid var(--line);
      background: var(--surface);
      color: var(--text-muted);
      padding: 8px 12px;
      border-radius: 10px;
      font-weight: 600;
      cursor: pointer;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 24px 20px 42px;
      display: grid;
      gap: 18px;
    }
    .hero {
      background: linear-gradient(130deg, #ffffff 0%, #faf6ef 100%);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 28px;
      box-shadow: var(--shadow);
      display: flex;
      justify-content: space-between;
      align-items: end;
      gap: 18px;
      flex-wrap: wrap;
    }
    .hero h1 {
      margin: 0;
      font-size: clamp(30px, 3vw, 42px);
      line-height: 1.1;
      letter-spacing: -0.3px;
    }
    .hero p {
      margin: 10px 0 0;
      color: var(--text-muted);
      font-size: 17px;
      max-width: 740px;
    }
    .hero-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .btn {
      border: none;
      border-radius: 12px;
      padding: 11px 16px;
      cursor: pointer;
      font-weight: 700;
      font-size: 14px;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }
    .btn-primary {
      color: #fff;
      background: linear-gradient(120deg, var(--brand), var(--brand-strong));
      box-shadow: 0 10px 20px rgba(71, 56, 190, 0.25);
    }
    .btn-secondary {
      color: var(--text);
      background: #fff;
      border: 1px solid var(--line-strong);
    }
    .btn-ghost {
      background: #fff;
      border: 1px solid var(--line);
      color: var(--text-muted);
    }
    .panel-grid {
      display: grid;
      grid-template-columns: 1.75fr 1fr;
      gap: 18px;
      align-items: start;
    }
    .card {
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 16px;
      box-shadow: var(--shadow);
      padding: 18px;
    }
    .card h2, .card h3 {
      margin: 0;
      font-size: 22px;
      letter-spacing: -0.2px;
    }
    .card h3 { font-size: 19px; }
    .muted { color: var(--text-muted); }
    .tiny { font-size: 12px; }
    .status-box {
      margin-top: 12px;
      border: 1px solid var(--line);
      background: var(--surface-soft);
      border-radius: 12px;
      padding: 10px 12px;
      min-height: 52px;
      font-size: 14px;
    }
    .assistant-head {
      margin-top: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .progress-label {
      font-weight: 700;
      font-size: 13px;
      color: #5c554d;
    }
    .progress {
      margin-top: 8px;
      width: 100%;
      height: 10px;
      border-radius: 999px;
      background: #efe8dc;
      overflow: hidden;
    }
    .progress-bar {
      height: 100%;
      width: 0;
      background: linear-gradient(90deg, #7a66e7, #5a49d6);
      transition: width 240ms ease;
    }
    .step-tags {
      margin-top: 12px;
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 8px;
    }
    .step-tag {
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #fbf8f3;
      color: #756d64;
      text-align: center;
      padding: 6px 8px;
      font-size: 12px;
      font-weight: 700;
    }
    .step-tag.active {
      border-color: #b7aae8;
      color: #3d2faf;
      background: #f0ebff;
    }
    .ai-prompt {
      margin-top: 14px;
      border: 1px solid #ddd2c2;
      background: #fff9ef;
      border-radius: 14px;
      padding: 12px 14px;
    }
    .ai-prompt .label {
      color: #7d6542;
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.7px;
      margin-bottom: 4px;
    }
    .field-grid {
      margin-top: 14px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    .full { grid-column: 1 / -1; }
    label {
      display: block;
      margin-bottom: 6px;
      font-size: 12px;
      color: #6f665d;
      font-weight: 700;
    }
    input, textarea, select {
      width: 100%;
      border: 1px solid #d9cec0;
      border-radius: 11px;
      padding: 10px 11px;
      background: #fff;
      color: var(--text);
      font: inherit;
    }
    textarea {
      min-height: 94px;
      resize: vertical;
    }
    input:focus, textarea:focus, select:focus {
      border-color: #9e8fea;
      box-shadow: 0 0 0 3px rgba(122, 102, 231, 0.12);
      outline: none;
    }
    .chips {
      margin-top: 10px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .chip {
      border: 1px solid #dbcfc0;
      background: #fff;
      color: #63574c;
      border-radius: 999px;
      padding: 7px 11px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
    }
    .controls {
      margin-top: 14px;
      display: flex;
      justify-content: space-between;
      gap: 8px;
      flex-wrap: wrap;
    }
    .brief-list {
      margin: 0;
      padding: 0;
      list-style: none;
      display: grid;
      gap: 8px;
      margin-top: 12px;
    }
    .brief-list li {
      border: 1px solid var(--line);
      border-radius: 11px;
      padding: 10px;
      background: #fffcf8;
      font-size: 14px;
    }
    .brief-list strong {
      display: block;
      margin-bottom: 2px;
      font-size: 13px;
      color: #4f473e;
    }
    .follow-up {
      margin-top: 12px;
      border: 1px solid var(--line);
      border-radius: 11px;
      padding: 10px;
      background: #fff;
    }
    .follow-up ul {
      margin: 8px 0 0;
      padding-left: 18px;
      color: var(--text-muted);
      font-size: 14px;
    }
    .readiness {
      margin-top: 12px;
      border: 1px solid var(--line);
      border-radius: 11px;
      background: var(--surface-soft);
      padding: 10px;
    }
    .sow-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 12px;
    }
    .sow-grid .full {
      grid-column: 1 / -1;
    }
    .sow-actions {
      margin-top: 12px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .section-head {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 8px;
      flex-wrap: wrap;
    }
    .requests-grid {
      margin-top: 12px;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    .request-card {
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 12px;
      background: #fff;
      display: grid;
      gap: 8px;
    }
    .status-pill {
      display: inline-flex;
      border-radius: 999px;
      padding: 5px 9px;
      font-size: 11px;
      font-weight: 700;
      border: 1px solid #d8ccbd;
      color: #695f53;
      background: #faf4eb;
    }
    .empty {
      margin-top: 12px;
      border: 1px dashed var(--line-strong);
      border-radius: 12px;
      padding: 14px;
      color: var(--text-muted);
      background: #fffdfa;
    }
    .drawer-overlay {
      position: fixed;
      inset: 0;
      background: rgba(27, 22, 15, 0.34);
      z-index: 8;
      display: none;
    }
    .drawer-overlay.open { display: block; }
    .drawer {
      position: fixed;
      top: 0;
      right: 0;
      width: min(430px, 100%);
      height: 100vh;
      background: #fff;
      border-left: 1px solid var(--line);
      box-shadow: -20px 0 40px rgba(33, 26, 17, 0.15);
      z-index: 9;
      transform: translateX(105%);
      transition: transform 240ms ease;
      padding: 18px;
      overflow-y: auto;
    }
    .drawer.open { transform: translateX(0%); }
    .drawer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }
    .drawer h3 { margin: 0; }
    .notice-success {
      border: 1px solid #c8e2d2;
      background: var(--success-bg);
      color: var(--success);
    }
    .notice-warning {
      border: 1px solid #f1deb0;
      background: var(--warning-bg);
      color: var(--warning);
    }
    .hidden { display: none; }
    @media (max-width: 1040px) {
      .panel-grid { grid-template-columns: 1fr; }
      .step-tags { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      .requests-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 760px) {
      .hero { padding: 20px; }
      .field-grid, .sow-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <nav class="top-nav">
    <div class="top-nav-inner">
      <div class="brand">
        <span class="brand-mark">MJ</span>
        <span>Matt James Client Portal</span>
      </div>
      <div class="nav-links">
        <button id="navStartBtn">Start new request</button>
        <button id="navRequestsBtn">My requests</button>
        <button id="navHelpBtn">Help</button>
        <button id="openSettingsBtn">Settings</button>
      </div>
    </div>
  </nav>

  <div class="container">
    <section class="hero">
      <div>
        <h1>Tell us what you want to build.</h1>
        <p>Our AI intake assistant will help shape your idea into a clear project scope and Statement of Work.</p>
      </div>
      <div class="hero-actions">
        <button class="btn btn-primary" id="heroStartBtn">Start a new request</button>
        <button class="btn btn-secondary" id="heroRequestsBtn">View my requests</button>
      </div>
    </section>

    <div class="panel-grid">
      <div class="card">
        <div class="section-head">
          <h2>AI Intake Assistant</h2>
          <div class="muted tiny">Guided intake from idea to project brief</div>
        </div>
        <div id="intakeStatus" class="status-box">Start by describing what you want to build. We will guide you step-by-step.</div>
        <div class="assistant-head">
          <div class="progress-label" id="progressLabel">Progress: 1 of 6</div>
          <div class="tiny muted" id="readinessHint">SOW readiness: 0%</div>
        </div>
        <div class="progress" aria-hidden="true">
          <div class="progress-bar" id="intakeProgress"></div>
        </div>
        <div class="step-tags">
          <div id="indicator-0" class="step-tag active">Basics</div>
          <div id="indicator-1" class="step-tag">Users</div>
          <div id="indicator-2" class="step-tag">Workflow</div>
          <div id="indicator-3" class="step-tag">Systems</div>
          <div id="indicator-4" class="step-tag">Delivery</div>
          <div id="indicator-5" class="step-tag">Review</div>
        </div>

        <div class="ai-prompt">
          <div class="label">Current AI question</div>
          <div id="aiQuestion">What is the app, workflow, or tool you want us to help you build?</div>
        </div>

        <div id="step-0">
          <div class="field-grid">
            <div>
              <label for="title">Project title</label>
              <input id="title" placeholder="Example: Sales onboarding automation workspace" />
            </div>
            <div>
              <label for="request_type">Type of request</label>
              <select id="request_type">
                <option value="new_app">New app</option>
                <option value="workflow_automation">Workflow automation</option>
                <option value="dashboard_report">Dashboard/report</option>
                <option value="ai_assistant">AI assistant</option>
                <option value="integration">Integration</option>
                <option value="website_portal">Website/client portal</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div class="full">
              <label for="goal">What are you trying to achieve?</label>
              <textarea id="goal" placeholder="Describe the business problem and what success would look like."></textarea>
            </div>
          </div>
        </div>

        <div id="step-1" class="hidden">
          <div class="field-grid">
            <div class="full">
              <label for="primary_users">Who are the primary users?</label>
              <textarea id="primary_users" placeholder="Who will use this first? Include teams, roles, or customer groups."></textarea>
            </div>
            <div class="full">
              <label for="user_actions">What do users need to do in this solution?</label>
              <textarea id="user_actions" placeholder="Example: submit intake forms, review requests, approve deliverables."></textarea>
            </div>
          </div>
        </div>

        <div id="step-2" class="hidden">
          <div class="field-grid">
            <div class="full">
              <label for="current_process">What does your current workflow look like?</label>
              <textarea id="current_process" placeholder="Describe the process today and where it breaks down."></textarea>
            </div>
            <div class="full">
              <label for="features">Desired features</label>
              <textarea id="features" placeholder="List the must-have features first."></textarea>
            </div>
          </div>
        </div>

        <div id="step-3" class="hidden">
          <div class="field-grid">
            <div class="full">
              <label for="systems">What systems, tools, or data sources should this connect to?</label>
              <textarea id="systems" placeholder="Examples: Salesforce, QuickBooks, HubSpot, Google Sheets, internal database."></textarea>
            </div>
            <div class="full">
              <label for="assets">Attachments or examples</label>
              <textarea id="assets" placeholder="Paste links to docs, examples, screenshots, and notes."></textarea>
            </div>
            <div class="full">
              <label for="security">Security, compliance, or approval needs</label>
              <textarea id="security" placeholder="Examples: SOC 2, HIPAA, role-based access, legal approval, audit trail."></textarea>
            </div>
          </div>
        </div>

        <div id="step-4" class="hidden">
          <div class="field-grid">
            <div>
              <label for="timeline">Timeline target</label>
              <input id="timeline" placeholder="Example: Pilot in 6 weeks, launch in 10 weeks" />
            </div>
            <div>
              <label for="budget">Budget range or urgency</label>
              <input id="budget" placeholder="Example: $25k-$40k, high urgency this quarter" />
            </div>
            <div class="full">
              <label for="success">Definition of success after launch</label>
              <textarea id="success" placeholder="How will you know this project was successful?"></textarea>
            </div>
          </div>
        </div>

        <div id="step-5" class="hidden">
          <div class="status-box notice-success">
            Review your project brief, then create the Statement of Work preview.
          </div>
          <div class="field-grid">
            <div class="full">
              <label for="project_brief_review">Project brief review notes</label>
              <textarea id="project_brief_review" placeholder="Optional notes before final submission."></textarea>
            </div>
          </div>
        </div>

        <div class="chips" id="quickChips"></div>
        <div class="controls">
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <button id="backBtn" class="btn btn-ghost">Back</button>
            <button id="nextBtn" class="btn btn-primary">Next</button>
          </div>
          <button id="saveDraftBtn" class="btn btn-secondary">Save draft</button>
        </div>
      </div>

      <aside>
        <div class="card">
          <h3>Live Project Brief</h3>
          <div class="muted tiny">Your request summary updates as you answer.</div>
          <ul class="brief-list">
            <li><strong>Goal</strong><span id="briefGoal">Add your project goal to begin.</span></li>
            <li><strong>Users</strong><span id="briefUsers">Describe who this solution supports.</span></li>
            <li><strong>Core features</strong><span id="briefFeatures">List must-have features in plain language.</span></li>
            <li><strong>Integrations</strong><span id="briefIntegrations">Mention systems and data sources to connect.</span></li>
            <li><strong>Open questions</strong><span id="briefOpenQuestions">AI follow-up questions will appear here.</span></li>
            <li><strong>Risks / assumptions</strong><span id="briefRisks">Security, timeline, or scope assumptions.</span></li>
            <li><strong>Suggested next step</strong><span id="briefNextStep">Complete basics to unlock smarter follow-up guidance.</span></li>
          </ul>
          <div class="follow-up">
            <strong>AI refining questions</strong>
            <ul id="followUpList">
              <li>Who are the primary users?</li>
              <li>What problem should this solve first?</li>
            </ul>
          </div>
          <div class="readiness">
            <strong>SOW readiness</strong>
            <div class="muted tiny" id="sowReadinessText">Complete key intake answers to generate a polished SOW preview.</div>
          </div>
        </div>
      </aside>
    </div>

    <section class="card">
      <div class="section-head">
        <h2>Statement of Work Preview</h2>
        <button class="btn btn-secondary" id="generateSowBtn">Generate from intake</button>
      </div>
      <div class="muted">Review and edit this draft before submitting for our team review.</div>
      <div class="sow-grid">
        <div class="full"><label for="sowExecutive">Executive summary</label><textarea id="sowExecutive"></textarea></div>
        <div><label for="sowObjectives">Project objectives</label><textarea id="sowObjectives"></textarea></div>
        <div><label for="sowScope">Scope of work</label><textarea id="sowScope"></textarea></div>
        <div><label for="sowFeatures">Key features</label><textarea id="sowFeatures"></textarea></div>
        <div><label for="sowRoles">User roles</label><textarea id="sowRoles"></textarea></div>
        <div><label for="sowIntegrations">Integrations / systems involved</label><textarea id="sowIntegrations"></textarea></div>
        <div><label for="sowDeliverables">Deliverables</label><textarea id="sowDeliverables"></textarea></div>
        <div><label for="sowAssumptions">Assumptions</label><textarea id="sowAssumptions"></textarea></div>
        <div><label for="sowOutOfScope">Out-of-scope items</label><textarea id="sowOutOfScope"></textarea></div>
        <div><label for="sowTimeline">Timeline / milestones</label><textarea id="sowTimeline"></textarea></div>
        <div><label for="sowResponsibilities">Client responsibilities</label><textarea id="sowResponsibilities"></textarea></div>
        <div><label for="sowAcceptance">Acceptance criteria</label><textarea id="sowAcceptance"></textarea></div>
        <div><label for="sowOpenQuestions">Open questions</label><textarea id="sowOpenQuestions"></textarea></div>
        <div><label for="sowPricing">Pricing</label><textarea id="sowPricing">To be estimated after review.</textarea></div>
      </div>
      <div class="sow-actions">
        <button id="submitRequestBtn" class="btn btn-primary">Review and submit</button>
        <button id="approveSowBtn" class="btn btn-secondary">Approve SOW</button>
        <button id="requestChangesBtn" class="btn btn-ghost">Request changes</button>
      </div>
      <div id="result" class="status-box">Your request progress and submission updates will appear here.</div>
    </section>

    <section class="card" id="requestsSection">
      <div class="section-head">
        <h2>My Requests</h2>
        <button id="refreshBtn" class="btn btn-secondary">Refresh list</button>
      </div>
      <div class="muted">Track your requests, continue drafts, and review SOW progress.</div>
      <div id="requestsGrid" class="requests-grid"></div>
      <div id="requestsEmpty" class="empty">No requests yet. Start a new request to create your first project brief.</div>
    </section>

    <section class="card">
      <div class="section-head">
        <h2>SOW Review Actions</h2>
        <div class="muted tiny">Use this area once a preview is available.</div>
      </div>
      <div class="field-grid">
        <div>
          <label for="preview_request_select">Select request</label>
          <select id="preview_request_select"><option value="">Select a request...</option></select>
        </div>
        <div>
          <label for="preview_decision">Decision</label>
          <select id="preview_decision">
            <option value="approve">Approve SOW</option>
            <option value="request_changes">Request changes</option>
            <option value="reject">Decline request</option>
          </select>
        </div>
      </div>
      <div class="sow-actions">
        <button id="loadPreviewBtn" class="btn btn-secondary">Load SOW preview details</button>
        <a id="openPreviewLink" href="#" target="_blank" style="display:none" class="btn btn-ghost">Open preview</a>
      </div>
      <div style="margin-top:10px">
        <label for="preview_feedback">Feedback for our delivery team</label>
        <textarea id="preview_feedback" placeholder="Share what you want changed, clarified, or approved."></textarea>
      </div>
      <div class="sow-actions"><button id="submitDecisionBtn" class="btn btn-primary">Submit SOW decision</button></div>
      <div id="previewMeta" class="status-box">Select a request to load preview details.</div>
    </section>
  </div>

  <div class="drawer-overlay" id="drawerOverlay"></div>
  <aside class="drawer" id="settingsDrawer">
    <div class="drawer-header">
      <h3>Admin / Developer Settings</h3>
      <button id="closeSettingsBtn" class="btn btn-ghost">Close</button>
    </div>
    <div class="muted">These settings are for internal configuration and are hidden from client-facing workflow.</div>
    <div class="field-grid" style="margin-top:12px">
      <div class="full"><label for="base_url">API base URL</label><input id="base_url" value="http://127.0.0.1:8000" /></div>
      <div class="full"><label for="api_key">API key</label><input id="api_key" placeholder="Internal API key" /></div>
      <div class="full"><label for="organization_id">Organization ID</label><input id="organization_id" placeholder="Internal organization identifier" /></div>
      <div class="full"><label for="project_id">Project ID (optional)</label><input id="project_id" placeholder="Optional internal project identifier" /></div>
    </div>
  </aside>

  <script>
    const steps = [0, 1, 2, 3, 4, 5];
    const stepQuestions = [
      "What is the app, workflow, or tool you want us to help you build?",
      "Who are the primary users, and what do they need to accomplish?",
      "What does your current process look like, and what should improve first?",
      "What systems should this connect to, and what constraints should we plan for?",
      "What timeline, urgency, and success metrics should guide this project?",
      "Would you like to submit this project brief and SOW draft for review?"
    ];
    const stepChipSuggestions = [
      ["A client onboarding portal", "An internal KPI dashboard", "Automate approval workflow"],
      ["Sales and operations teams", "Managers need weekly visibility", "Clients approve deliverables"],
      ["Current process is manual email", "Need single source of truth", "Too many handoffs today"],
      ["Connect Salesforce and Slack", "Pull data from Google Sheets", "Needs role-based access"],
      ["Pilot in 6 weeks", "Need launch this quarter", "Success = faster turnaround"],
      ["Save as draft first", "Generate SOW now", "Submit for team review"]
    ];
    let stepIndex = 0;
    let cachedRequests = [];
    let selectedPreviewBuild = null;
    let latestRequestId = null;

    function byId(id) { return document.getElementById(id); }

    function intakeData() {
      return {
        title: byId("title").value.trim(),
        request_type: byId("request_type").value,
        goal: byId("goal").value.trim(),
        primary_users: byId("primary_users").value.trim(),
        user_actions: byId("user_actions").value.trim(),
        current_process: byId("current_process").value.trim(),
        features: byId("features").value.trim(),
        systems: byId("systems").value.trim(),
        assets: byId("assets").value.trim(),
        security: byId("security").value.trim(),
        timeline: byId("timeline").value.trim(),
        budget: byId("budget").value.trim(),
        success: byId("success").value.trim(),
        project_brief_review: byId("project_brief_review").value.trim()
      };
    }

    function requestPayload() {
      const form = intakeData();
      const detailsParts = [];
      if (form.primary_users) detailsParts.push("Primary users:\\n" + form.primary_users);
      if (form.user_actions) detailsParts.push("User actions:\\n" + form.user_actions);
      if (form.current_process) detailsParts.push("Current process:\\n" + form.current_process);
      if (form.features) detailsParts.push("Desired features:\\n" + form.features);
      if (form.systems) detailsParts.push("Systems and data sources:\\n" + form.systems);
      if (form.assets) detailsParts.push("Attachments/examples:\\n" + form.assets);
      if (form.security) detailsParts.push("Security and compliance:\\n" + form.security);
      if (form.timeline) detailsParts.push("Timeline:\\n" + form.timeline);
      if (form.budget) detailsParts.push("Budget / urgency:\\n" + form.budget);
      if (form.success) detailsParts.push("Definition of success:\\n" + form.success);
      if (form.project_brief_review) detailsParts.push("Client review notes:\\n" + form.project_brief_review);

      const payload = {
        organization_id: byId("organization_id").value.trim(),
        request_type: form.request_type,
        title: form.title,
        goal: form.goal,
        details: detailsParts.join("\\n\\n") || null
      };
      const projectId = byId("project_id").value.trim();
      if (projectId) payload.project_id = projectId;
      return payload;
    }

    function completionPercent() {
      const form = intakeData();
      const required = [form.title, form.goal, form.primary_users, form.user_actions, form.current_process, form.features, form.systems, form.security, form.timeline, form.success];
      const completed = required.filter(item => item).length;
      return Math.round((completed / required.length) * 100);
    }

    function humanRequestType(value) {
      const mapping = {
        new_app: "New app",
        workflow_automation: "Workflow automation",
        dashboard_report: "Dashboard/report",
        ai_assistant: "AI assistant",
        integration: "Integration",
        website_portal: "Website/client portal",
        update: "Update",
        bugfix: "Bugfix",
        enhancement: "Enhancement",
        other: "Other"
      };
      return mapping[value] || value || "Unspecified";
    }

    function humanStatus(status) {
      const mapping = {
        draft: "Draft",
        submitted: "Submitted",
        triaged: "Needs more detail",
        building: "In review",
        preview_ready: "SOW ready for review",
        client_review: "SOW ready for review",
        changes_requested: "Changes requested",
        approved: "Approved",
        rejected: "Changes requested"
      };
      return mapping[status] || String(status || "draft").replaceAll("_", " ");
    }

    function actionLabel(status) {
      const value = humanStatus(status).toLowerCase();
      if (value.includes("draft") || value.includes("detail")) return "Continue";
      if (value.includes("sow") || value.includes("review")) return "Review SOW";
      return "View details";
    }

    function setStatusMessage(text, noticeClass) {
      const el = byId("result");
      el.classList.remove("notice-success", "notice-warning");
      if (noticeClass) el.classList.add(noticeClass);
      el.textContent = text;
    }

    function buildAiFollowUps() {
      const form = intakeData();
      const followUps = [];
      if (!form.primary_users) followUps.push("Who are the primary users we should prioritize?");
      if (!form.current_process) followUps.push("What does your current workflow look like today?");
      if (!form.systems) followUps.push("What systems does this solution need to connect with?");
      if (!form.success) followUps.push("What would make this project successful after launch?");
      if (!form.security) followUps.push("Any compliance, privacy, or approval requirements?");
      if (!form.timeline) followUps.push("When do you need an initial version in users' hands?");
      if (followUps.length === 0) followUps.push("Great detail so far. Do you want a pilot-first plan or full launch plan?");
      return followUps.slice(0, 4);
    }

    function updateLiveBrief() {
      const form = intakeData();
      const followUps = buildAiFollowUps();
      byId("briefGoal").textContent = form.goal || "Add your project goal to begin.";
      byId("briefUsers").textContent = form.primary_users || "Describe who this solution supports.";
      byId("briefFeatures").textContent = form.features || "List must-have features in plain language.";
      byId("briefIntegrations").textContent = form.systems || "Mention systems and data sources to connect.";
      byId("briefOpenQuestions").textContent = followUps.join(" ");

      const riskHints = [];
      if (!form.security) riskHints.push("Security/compliance requirements still needed.");
      if (!form.timeline) riskHints.push("Timeline is not yet defined.");
      if (!form.budget) riskHints.push("Budget/urgency has not been clarified.");
      byId("briefRisks").textContent = riskHints.length ? riskHints.join(" ") : "Known constraints are documented.";

      const readiness = completionPercent();
      byId("briefNextStep").textContent = readiness < 50
        ? "Continue the intake so we can shape scope and recommendations."
        : "Generate your SOW preview, review details, then submit.";
      byId("sowReadinessText").textContent = readiness + "% complete. " + (readiness >= 80 ? "Ready for strong SOW draft." : "Add more detail for a stronger first draft.");
      byId("readinessHint").textContent = "SOW readiness: " + readiness + "%";
      byId("followUpList").innerHTML = followUps.map(item => "<li>" + item + "</li>").join("");
    }

    function bindFieldListeners() {
      const fieldIds = ["title", "request_type", "goal", "primary_users", "user_actions", "current_process", "features", "systems", "assets", "security", "timeline", "budget", "success", "project_brief_review"];
      fieldIds.forEach((fieldId) => {
        byId(fieldId).addEventListener("input", () => {
          updateLiveBrief();
          updateStepUi();
        });
      });
    }

    function updateQuickChips() {
      const chipsWrap = byId("quickChips");
      const suggestions = stepChipSuggestions[stepIndex];
      chipsWrap.innerHTML = suggestions.map((text) => '<button class="chip">' + text + "</button>").join("");
      chipsWrap.querySelectorAll(".chip").forEach((btn) => {
        btn.addEventListener("click", () => {
          const selectedText = btn.textContent;
          const targetField = ({0: "goal", 1: "primary_users", 2: "current_process", 3: "systems", 4: "success", 5: "project_brief_review"})[stepIndex];
          const field = byId(targetField);
          if (field) {
            field.value = field.value ? field.value + "\\n- " + selectedText : selectedText;
            field.dispatchEvent(new Event("input"));
          }
        });
      });
    }

    function gatherSowDraft() {
      const form = intakeData();
      const followUps = buildAiFollowUps();
      return {
        executive: (form.title || "Requested project") + " is a " + humanRequestType(form.request_type).toLowerCase() + " initiative focused on " + (form.goal || "solving the stated business challenge") + ".",
        objectives: ["Clarify and document business outcomes for launch readiness.", "Design a client-friendly workflow for " + (form.primary_users || "target users") + ".", "Prioritize quick wins while creating a scalable foundation."].join("\\n"),
        scope: ["- Discovery and requirement refinement workshop", "- UX workflow and intake-to-delivery blueprint", "- Build and configuration of priority feature set", "- Stakeholder review and revision cycle"].join("\\n"),
        features: form.features || "Feature list to be finalized from intake discussion.",
        roles: form.primary_users || "Primary user roles to be confirmed.",
        integrations: form.systems || "Integration details to be confirmed.",
        deliverables: ["- Approved project brief", "- Statement of Work", "- Interactive build plan", "- Delivery roadmap and milestones"].join("\\n"),
        assumptions: form.security ? "Assumes requirements include: " + form.security : "Assumes standard security and access controls unless otherwise specified.",
        outOfScope: "Long-term support, net-new third-party licensing, and non-approved integrations.",
        timeline: form.timeline || "Timeline to be finalized after scoping workshop.",
        responsibilities: "Client provides timely feedback, stakeholder approvals, and required system access.",
        acceptance: form.success || "Acceptance criteria to be finalized during scope review.",
        openQuestions: followUps.join("\\n"),
        pricing: "To be estimated after review."
      };
    }

    function generateSowPreview() {
      const draft = gatherSowDraft();
      byId("sowExecutive").value = draft.executive;
      byId("sowObjectives").value = draft.objectives;
      byId("sowScope").value = draft.scope;
      byId("sowFeatures").value = draft.features;
      byId("sowRoles").value = draft.roles;
      byId("sowIntegrations").value = draft.integrations;
      byId("sowDeliverables").value = draft.deliverables;
      byId("sowAssumptions").value = draft.assumptions;
      byId("sowOutOfScope").value = draft.outOfScope;
      byId("sowTimeline").value = draft.timeline;
      byId("sowResponsibilities").value = draft.responsibilities;
      byId("sowAcceptance").value = draft.acceptance;
      byId("sowOpenQuestions").value = draft.openQuestions;
      byId("sowPricing").value = draft.pricing;
      setStatusMessage("SOW preview refreshed from your latest intake answers.", "notice-success");
    }

    function updateStepUi() {
      for (const idx of steps) {
        byId("step-" + idx).classList.toggle("hidden", idx !== stepIndex);
        byId("indicator-" + idx).classList.toggle("active", idx === stepIndex);
      }
      byId("backBtn").disabled = stepIndex === 0;
      byId("nextBtn").textContent = stepIndex === 5 ? "Generate SOW + Review" : "Next";
      byId("aiQuestion").textContent = stepQuestions[stepIndex];
      byId("progressLabel").textContent = "Progress: " + (stepIndex + 1) + " of 6";
      byId("intakeProgress").style.width = (((stepIndex + 1) / steps.length) * 100) + "%";
      updateQuickChips();
      updateLiveBrief();
      if (stepIndex === 5 && !byId("sowExecutive").value.trim()) generateSowPreview();
    }

    async function submitRequest() {
      const payload = requestPayload();
      const base = byId("base_url").value.trim();
      const key = byId("api_key").value.trim();
      if (!payload.organization_id || !payload.title || !payload.goal) {
        setStatusMessage("Please complete project title, goal, and internal organization settings before submitting.", "notice-warning");
        return;
      }
      setStatusMessage("Submitting your request...", null);
      const confirmed = window.confirm("Submit this request for review now?");
      if (!confirmed) {
        setStatusMessage("Submission canceled. Your draft is still available.", "notice-warning");
        return;
      }
      try {
        const res = await fetch(base + "/v1/intake-requests", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": key,
            "Idempotency-Key": "client-req-" + Date.now()
          },
          body: JSON.stringify(payload)
        });
        const body = await res.json();
        if (res.status >= 200 && res.status < 300) {
          latestRequestId = body && body.id ? body.id : null;
          setStatusMessage("Request submitted. Your team will review and return with a scoped SOW plan.", "notice-success");
          stepIndex = 0;
          updateStepUi();
          await refreshRequests();
        } else {
          const message = body && body.error && body.error.message ? body.error.message : "We could not submit your request right now. Please try again.";
          setStatusMessage("Submission failed: " + message, "notice-warning");
        }
      } catch (_err) {
        setStatusMessage("Submission failed due to a network error. Please try again.", "notice-warning");
      }
    }

    function decisionToStatus(decision) {
      if (decision === "approve") return "approved";
      if (decision === "request_changes") return "changes_requested";
      return "rejected";
    }

    async function refreshRequests() {
      const base = byId("base_url").value.trim();
      const key = byId("api_key").value.trim();
      const orgId = byId("organization_id").value.trim();
      const requestSelect = byId("preview_request_select");
      const requestsGrid = byId("requestsGrid");
      const requestsEmpty = byId("requestsEmpty");
      if (!orgId) {
        requestsGrid.innerHTML = "";
        requestsEmpty.style.display = "block";
        requestsEmpty.textContent = "Open admin settings to set your organization before loading requests.";
        requestSelect.innerHTML = '<option value="">Select a request...</option>';
        cachedRequests = [];
        return;
      }
      try {
        const res = await fetch(base + "/v1/intake-requests?organization_id=" + encodeURIComponent(orgId), {headers: {"X-API-Key": key}});
        const body = await res.json();
        if (res.status < 200 || res.status >= 300 || !Array.isArray(body)) {
          requestsGrid.innerHTML = "";
          requestsEmpty.style.display = "block";
          requestsEmpty.textContent = "We could not load your requests right now.";
          requestSelect.innerHTML = '<option value="">Select a request...</option>';
          cachedRequests = [];
          return;
        }
        if (body.length === 0) {
          requestsGrid.innerHTML = "";
          requestsEmpty.style.display = "block";
          requestsEmpty.textContent = "No requests yet. Start a new request to create your first project brief.";
          requestSelect.innerHTML = '<option value="">Select a request...</option>';
          cachedRequests = [];
          return;
        }
        cachedRequests = body;
        requestsEmpty.style.display = "none";
        requestSelect.innerHTML = '<option value="">Select a request...</option>' + body.map(item => '<option value="' + item.id + '">' + item.title + " (" + humanStatus(item.status) + ")</option>").join("");
        requestsGrid.innerHTML = body.map(item => (
          '<div class="request-card">' +
            '<div style="display:flex;justify-content:space-between;gap:8px;align-items:center">' +
              '<strong>' + item.title + "</strong>" +
              '<span class="status-pill">' + humanStatus(item.status) + "</span>" +
            "</div>" +
            '<div class="tiny muted">Type: ' + humanRequestType(item.request_type) + "</div>" +
            '<div class="tiny muted">Last updated: ' + item.updated_at + "</div>" +
            '<div class="tiny muted">Current stage: ' + humanStatus(item.status) + "</div>" +
            '<div><button class="btn btn-ghost request-action" data-request-id="' + item.id + '">' + actionLabel(item.status) + "</button></div>" +
          "</div>"
        )).join("");
        document.querySelectorAll(".request-action").forEach((btn) => {
          btn.addEventListener("click", () => {
            byId("preview_request_select").value = btn.getAttribute("data-request-id");
            byId("requestsSection").scrollIntoView({behavior: "smooth", block: "start"});
            setStatusMessage("Request selected. Load preview details or continue refining the intake.", null);
          });
        });
      } catch (_err) {
        requestsGrid.innerHTML = "";
        requestsEmpty.style.display = "block";
        requestsEmpty.textContent = "We could not load your requests right now.";
        requestSelect.innerHTML = '<option value="">Select a request...</option>';
        cachedRequests = [];
      }
    }

    async function loadPreviewForSelectedRequest() {
      const base = byId("base_url").value.trim();
      const key = byId("api_key").value.trim();
      const intakeRequestId = byId("preview_request_select").value;
      const meta = byId("previewMeta");
      const openLink = byId("openPreviewLink");
      selectedPreviewBuild = null;
      openLink.style.display = "none";
      if (!intakeRequestId) {
        meta.textContent = "Select a request first, then load preview.";
        return;
      }
      try {
        const res = await fetch(base + "/v1/preview-builds?intake_request_id=" + encodeURIComponent(intakeRequestId), {headers: {"X-API-Key": key}});
        const body = await res.json();
        if (res.status < 200 || res.status >= 300 || !Array.isArray(body) || body.length === 0) {
          meta.textContent = "No preview is available yet for this request.";
          return;
        }
        selectedPreviewBuild = body[0];
        openLink.href = selectedPreviewBuild.preview_url;
        openLink.style.display = "inline-flex";
        meta.textContent = "Preview ready: version " + selectedPreviewBuild.build_version + ". You can now review the preview link.";
      } catch (_err) {
        meta.textContent = "Could not load preview details. Please try again.";
      }
    }

    async function submitPreviewDecision() {
      const base = byId("base_url").value.trim();
      const key = byId("api_key").value.trim();
      const intakeRequestId = byId("preview_request_select").value || latestRequestId;
      const decision = byId("preview_decision").value;
      const feedback = byId("preview_feedback").value.trim();
      const meta = byId("previewMeta");
      if (!intakeRequestId) {
        meta.textContent = "Select a request first.";
        return;
      }
      const nextStatus = decisionToStatus(decision);
      if (decision !== "approve") {
        const confirmed = window.confirm("This decision may require additional revisions. Continue?");
        if (!confirmed) {
          meta.textContent = "Decision canceled. No changes were made.";
          return;
        }
      }
      try {
        const res = await fetch(base + "/v1/intake-requests/" + intakeRequestId + "/status", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": key,
            "Idempotency-Key": "client-decision-" + intakeRequestId + "-" + Date.now()
          },
          body: JSON.stringify({status: nextStatus, feedback: feedback || null})
        });
        const body = await res.json();
        if (res.status >= 200 && res.status < 300) {
          if (decision === "approve") {
            meta.textContent = "Decision submitted: Approved. We will continue to release preparation.";
            setStatusMessage("SOW approved and shared with our team for next-step planning.", "notice-success");
          } else if (decision === "request_changes") {
            meta.textContent = "Decision submitted: Changes requested. Your feedback has been recorded.";
            setStatusMessage("Changes requested. Your notes were shared with our delivery team.", "notice-warning");
          } else {
            meta.textContent = "Decision submitted: Declined. Your team has been notified.";
            setStatusMessage("Request declined. You can start a new request anytime.", "notice-warning");
          }
        } else {
          const message = body && body.error && body.error.message ? body.error.message : "We could not submit your decision right now.";
          meta.textContent = "Decision failed: " + message;
        }
        await refreshRequests();
      } catch (_err) {
        meta.textContent = "Decision failed due to a network error. Please try again.";
      }
    }

    function openSettings() {
      byId("settingsDrawer").classList.add("open");
      byId("drawerOverlay").classList.add("open");
    }

    function closeSettings() {
      byId("settingsDrawer").classList.remove("open");
      byId("drawerOverlay").classList.remove("open");
    }

    function scrollToIntake() {
      byId("title").focus();
      window.scrollTo({top: 0, behavior: "smooth"});
    }

    byId("backBtn").addEventListener("click", () => {
      if (stepIndex > 0) {
        stepIndex -= 1;
        updateStepUi();
      }
    });

    byId("nextBtn").addEventListener("click", () => {
      if (stepIndex < 5) {
        stepIndex += 1;
        updateStepUi();
        return;
      }
      generateSowPreview();
      byId("sowExecutive").scrollIntoView({behavior: "smooth", block: "start"});
    });

    byId("saveDraftBtn").addEventListener("click", () => {
      setStatusMessage("Draft saved locally. Continue whenever you are ready.", "notice-success");
    });

    byId("generateSowBtn").addEventListener("click", generateSowPreview);
    byId("submitRequestBtn").addEventListener("click", submitRequest);
    byId("approveSowBtn").addEventListener("click", async () => {
      byId("preview_decision").value = "approve";
      await submitPreviewDecision();
    });
    byId("requestChangesBtn").addEventListener("click", async () => {
      byId("preview_decision").value = "request_changes";
      await submitPreviewDecision();
    });
    byId("refreshBtn").addEventListener("click", refreshRequests);
    byId("loadPreviewBtn").addEventListener("click", loadPreviewForSelectedRequest);
    byId("submitDecisionBtn").addEventListener("click", submitPreviewDecision);
    byId("openSettingsBtn").addEventListener("click", openSettings);
    byId("closeSettingsBtn").addEventListener("click", closeSettings);
    byId("drawerOverlay").addEventListener("click", closeSettings);
    byId("heroStartBtn").addEventListener("click", scrollToIntake);
    byId("heroRequestsBtn").addEventListener("click", () => byId("requestsSection").scrollIntoView({behavior: "smooth", block: "start"}));
    byId("navStartBtn").addEventListener("click", scrollToIntake);
    byId("navRequestsBtn").addEventListener("click", () => byId("requestsSection").scrollIntoView({behavior: "smooth", block: "start"}));
    byId("navHelpBtn").addEventListener("click", () => setStatusMessage("Need help? Start with your business goal and we will guide the rest.", null));

    bindFieldListeners();
    updateStepUi();
    refreshRequests();
  </script>
</body>
</html>
"""
