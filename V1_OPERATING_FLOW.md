# V1 Operating Flow (Frozen)

This document freezes the v1 operating flow for the Matt James platform and serves as the final reference for how the product is run today.

## Scope and Purpose

- Defines the operational journey from client intake to production deployment.
- Confirms role boundaries between Founder Console and Client Portal.
- Locks required backend guardrails for release and metering policy controls.
- Captures what is in scope for v1 and what should be deferred.

## Role Boundaries (Locked)

### Founder Console (internal only)

- Intake triage and prioritization.
- Preview build creation and preview status management.
- Approval decision management support.
- Release orchestration and release status updates.
- Client environment registry management.
- Metering policy controls.

### Client Portal (client-facing)

- Submit intake requests.
- Track request status.
- Review preview links.
- Submit approval decisions (`approve`, `request_changes`, `reject`).

### Boundary Rule

- Clients do not access founder/admin controls (release orchestration, metering policy, internal operations).

## Canonical Journey (v1)

1. Client submits intake request.
2. Founder triages request (owner, priority, status progress).
3. Founder creates preview build for request.
4. Founder marks preview build `ready`.
5. Client reviews preview and submits decision.
6. If decision is `request_changes`, flow loops back to step 3.
7. If decision is `approve`, founder creates release record.
8. Founder advances release to `deployed`.
9. Intake request reflects final `deployed` state.

## Backend Guardrails (Locked)

### Release creation requirements

- Preview build must belong to the intake request.
- Preview build must be `ready`.
- Latest approval decision must be `approve`.

### Metering controls

- Metering policy endpoints are founder/internal only.
- Tenant/client-scoped requests cannot modify metering policy.

### Tenant and write access

- Tenant scope checks are enforced for org-bound resources.
- Tenant write access is role-gated.
- Internal calls (non-tenant) are trusted for founder operations.

## v1 Data Surfaces (Operational)

- Intake requests
- Preview builds
- Approval decisions
- Release records
- Client environments
- Metering policies

## v1 Status Languages

### Intake request status

- `submitted`, `triaged`, `building`, `preview_ready`, `client_review`, `changes_requested`, `approved`, `deployed`, `rejected`

### Preview build status

- `queued`, `building`, `ready`, `failed`, `expired`

### Release status

- `pending`, `staged`, `approved`, `deployed`, `failed`, `rolled_back`

### Client environment status

- `provisioning`, `active`, `paused`, `failed`, `retired`

## Operational Endpoints (v1)

- Intake: `/v1/intake-requests`, `/v1/intake-requests/{id}/triage`, `/v1/intake-requests/{id}/status`
- Preview: `/v1/preview-builds`, `/v1/preview-builds/{id}/status`
- Approval: `/v1/approval-decisions`
- Releases: `/v1/releases`, `/v1/releases/{id}/status`
- Client environments: `/v1/client-environments`, `/v1/client-environments/{id}`
- Metering controls: `/v1/admin/metering/{organization_id}`

## Validation and Quality Bar

The v1 flow is considered valid only when all are true:

- Full demo journey test passes (intake -> build -> preview -> approval -> deploy).
- Release orchestration tests pass.
- Approval and preview flow tests pass.
- UX shells render and expose the expected flow surfaces.

## Out of Scope for v1 Freeze

- Advanced billing engine execution beyond policy storage/control.
- Multi-stage deployment automation beyond recorded release progression.
- Deep analytics dashboards and non-core reporting.
- Full notification orchestration.

## Change Control

- Treat this file as frozen for v1.
- Any behavior change to the above flow requires explicit versioned update (for example, v1.1) and matching test updates.
