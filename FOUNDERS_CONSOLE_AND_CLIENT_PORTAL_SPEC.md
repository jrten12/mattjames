# Founder Console + Client Portal Spec

## Short Answer: Does this tie into existing work?

Yes. This is an extension of what is already built, not a restart.

Current foundation already supports:

- org/project/app domain model
- role + tenant boundaries
- workflow transitions + event history
- idempotent writes + stable pagination
- demo bootstrap flow
- admin shell and admin control endpoints
- readiness and basic metrics

This spec layers product UX and request/release workflow on top of those rails.

---

## Product Surfaces

## 1) Founder Console (Matt + James only)

Purpose: Operate the platform, intake pipeline, preview pipeline, release, and policy controls.

### Primary navigation

1. Dashboard
2. Intake Queue
3. Clients
4. Apps
5. Preview & Approval
6. Releases
7. Metering Controls
8. Activity / Audit
9. Platform Settings

### Screen map (plain language)

#### Dashboard
- Today summary: open requests, builds in progress, pending approvals, failed deploys
- Health strip: API readiness, queue depth, active clients, high usage alerts
- Fast actions: Create request manually, open urgent item, retry failed deploy

#### Intake Queue
- Cards/table of client requests: New app, update, bugfix, enhancement
- Filters: client, status, urgency, app, submitted date
- Action panel: triage, assign owner, set target milestone, request clarification

#### Clients
- Client profile with owned apps, environments, domains, request history
- Client-level controls: active/paused, deployment policy, contact and notifications
- Usage overview (read-only first): current period usage and trend

#### Apps
- App catalog by client
- App status controls: draft, active, paused, retired
- Environment list: preview URL, production URL, version

#### Preview & Approval
- Side-by-side: build details + approval status
- Preview link manager: current preview build, expiry, access
- Approval actions: approve, request changes, reject with reason

#### Releases
- Release timeline: pending -> staged -> approved -> deployed
- One-click promote to production after approval
- Rollback controls and rollback reason capture

#### Metering Controls
- Backend-only controls for pricing and metering policy
- Per-client profile (phase rollout):
  - base fee policy
  - usage caps
  - overage behavior (allow/throttle/pause)
- This drives backend behavior; clients do not edit it

#### Activity / Audit
- Immutable timeline: who changed what, when, why
- Filter by client/app/request/release

#### Platform Settings
- API key rotation tools
- Tenant token and environment settings
- System readiness checks and alerts config

---

## 2) Client Portal (clients only)

Purpose: Submit requests, preview work, approve/reject, and track status. No backend controls.

### Primary navigation

1. New Request
2. My Requests
3. Preview Review
4. Releases (read-only)
5. Notifications

### Screen map

#### New Request
- Wizard:
  1. Request type (new app / update)
  2. Goal and business outcome
  3. Required features
  4. Assets and references
  5. Success criteria
  6. Submit

#### My Requests
- Status board: submitted, triaged, building, preview ready, waiting approval, deployed
- Each item has timeline and latest note

#### Preview Review
- Secure preview link
- Structured feedback form
- Decision: approve / request changes / reject

#### Releases
- List of approved and deployed versions
- What changed summary

#### Notifications
- New preview ready
- Approval requested
- Release completed

---

## Core Workflow (end-to-end)

1. Client submits intake request
2. Founder Console triages and plans work
3. Build is created and deployed to preview environment
4. Client reviews preview and approves or requests changes
5. Approved build is promoted to production client environment
6. Backend enforces metering/hosting/policy at runtime

Loop:
- If client requests changes, flow returns to build step and repeats

---

## Data/State Model Additions (next layer)

New entities to add on top of current model:

- intake_requests
- request_comments
- preview_builds
- approval_decisions
- release_records
- deployment_targets (client preview/prod environments)

Suggested request states:

- submitted
- triaged
- building
- preview_ready
- client_review
- changes_requested
- approved
- deployed
- rejected

---

## How this maps to current implementation

Already in place and reusable:

- `organizations`, `projects`, `apps` -> client and app ownership backbone
- workflow transitions/events -> request and release lifecycle logging base
- admin status endpoints -> early control actions
- demo bootstrap -> seed data for UI demos and pilot flows
- `/admin` shell -> can evolve into Founder Console

Add next:

- intake and approval endpoints
- preview build records and secure links
- release promotion endpoint
- client portal views backed by request/release entities

---

## Build Sequence (recommended)

### Wave 1: Intake + Tracking
- Add intake request model and endpoints
- Founder Queue UI
- Client request submission UI

### Wave 2: Preview + Approval
- Preview build records
- Approval/revision endpoints
- Client preview review screen

### Wave 3: Release Management
- Promote approved preview to production
- Rollback records and controls
- Release timeline in both portals

### Wave 4: Metering Console UX
- Founder-only metering policy screen
- Runtime policy enforcement hooks surfaced in UI

---

## Usability rules (non-programmer friendly)

- Step-by-step wizards for client inputs
- Plain language labels (no technical jargon)
- Safe defaults on all forms
- Clear statuses and next actions on every screen
- Confirmation dialogs for risky actions
- Everything important visible in one click from Dashboard
