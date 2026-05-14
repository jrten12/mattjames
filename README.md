# Matt James Platform API

Phase 1 implementation of the core platform foundation:

- Organizations, org members, projects, and apps (`/v1/orgs`, `/v1/orgs/{id}/members`, `/v1/projects`, `/v1/apps`)
- Non-linear workflow transitions and append-only project events
- API boundary auth and optional tenant JWT scoping
- Pagination/filtering on list endpoints (`limit`, `offset`, `cursor`, plus route-specific filters)
- Idempotent writes using `Idempotency-Key` header
- PostgreSQL schema baseline in `deploy/sql/multi_tenant_v1.sql`

## Frozen v1 operating flow

- Canonical v1 operating flow documentation: `V1_OPERATING_FLOW.md`
- UI/UX excellence standards for phase 2: `UI_UX_EXCELLENCE_SPEC.md`

## Quick start

1. Copy env file:

   ```bash
   cp .env.example .env
   ```

2. Install dependencies:

   ```bash
   uv sync
   ```

3. Apply schema in Postgres:

   ```bash
   psql "$DATABASE_URL" -f deploy/sql/multi_tenant_v1.sql
   ```

4. Optional schema smoke check:

   ```bash
   python scripts/check_db_schema.py
   ```

5. Run API:

   ```bash
   python -m uvicorn api.main:app --reload --port 8000
   ```

## Auth boundary

- `/health` is public.
- Every `/v1/*` route requires either:
  - `Authorization: Bearer <api_key>`, or
  - `X-API-Key: <api_key>`

If `ENFORCE_TENANT_JWT=true`, bearer token must be a valid tenant JWT and org-scoped routes reject cross-tenant access.
When tenant JWT is enabled, write operations also require role `client_owner`, `client_admin`, or `developer`.

## Workflow endpoints

- `POST /v1/projects/{id}/transitions`
- `GET /v1/projects/{id}/events`

Transitions are non-linear with guardrails enforced by the workflow service.

## Demo onboarding endpoint

- `POST /v1/demo/bootstrap` creates a full demo starter set in one call:
  - organization
  - owner member
  - project
  - app

Use this only for demos/sandbox setup.

## Admin UI shell

- Open `http://127.0.0.1:8000/admin` for a lightweight UI/UX shell.
- It can call `/v1/demo/bootstrap` directly so you can walk through demo onboarding.
- It also supports admin actions for project pause/resume and app status updates.

## Admin endpoints (v1)

- `GET /v1/admin/orgs/{organization_id}`
- `GET /v1/admin/projects/{project_id}`
- `GET /v1/admin/apps/{app_id}`
- `POST /v1/admin/projects/{project_id}/pause`
- `POST /v1/admin/projects/{project_id}/resume`
- `POST /v1/admin/apps/{app_id}/status`

## Release orchestration endpoints (v1)

- `POST /v1/releases` creates a release record from an approved preview build
- `GET /v1/releases?intake_request_id=...` lists release records for an intake request
- `POST /v1/releases/{release_id}/status` advances release state (`pending`, `staged`, `approved`, `deployed`, `failed`, `rolled_back`)

Release creation guardrails:

- preview build must belong to the intake request
- preview build must be in `ready` status
- latest approval decision for the intake request must be `approve`

## Client environment registry endpoints (v1)

- `POST /v1/client-environments` creates an environment record for an app
- `GET /v1/client-environments?app_id=...` lists environment records for that app
- `POST /v1/client-environments/{environment_id}` updates environment status/details

Environment supports:

- type: `preview`, `staging`, `production`
- status lifecycle: `provisioning`, `active`, `paused`, `failed`, `retired`

## Metering policy controls (founder-only)

- `POST /v1/admin/metering/{organization_id}` upserts org metering policy
- `GET /v1/admin/metering/{organization_id}` reads org metering policy

Policy fields:

- `base_fee_cents`
- `usage_cap`
- `overage_behavior` (`allow`, `throttle`, `pause`)
- `is_enforced`
- `notes`

These controls are restricted to internal/founder access (tenant clients cannot write them).

## Observability and readiness

- `GET /admin/metrics` returns in-process request counters (totals, by path, by status class).
- `GET /readyz` validates runtime readiness:
  - in-memory mode: always ready
  - Postgres mode: checks DB connectivity and returns `503` if unreachable

## Cursor pagination

List endpoints support stable ordering and cursor pagination using deterministic sort keys (`created_at`, `id`).
Pass `cursor` query param and read the `X-Next-Cursor` response header from the previous page.

## Tests

```bash
python -m pytest -v
```
