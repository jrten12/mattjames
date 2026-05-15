# Platform-native apps (“powered container”) — how we keep building

This document is the **north star** for continuing development: every customer lives in a **managed container** (org + projects + apps + environments + policy), and deliverables stay **attached** to Matt James—not handed off as disconnected binaries.

## What “powered” means

A customer container is **powered** when:

1. **Identity** — Every meaningful action can be attributed to `organization_id` (and usually `project_id` / `app_id`).
2. **Registry** — Apps and their preview/staging/production URLs are recorded (`apps`, `client_environments`).
3. **Lifecycle** — Changes flow through intake → preview → approval → release (already frozen in `V1_OPERATING_FLOW.md`).
4. **Metering (runtime)** — Usage is **observed** (or proxied), **aggregated**, and **enforced** against `metering_policies` (today: policy exists; **usage path is the gap to close**).
5. **Billing (commercial)** — Invoices/subscriptions map to the same org + usage dimensions (often Stripe or similar **outside** this API; Matt James holds truth for **usage + entitlements**).

Until (4) is real for the traffic path you care about, the container is **registered** but not fully **powered**.

## Where we develop client apps (configured by default)

Apps must not start as blank frameworks with no Matt James wiring. **Configuration is enforced by where and how we create repos**, not by memory at deploy time.

### Official recommendation (start here)

1. **Matt James App Template** — A single **GitHub template repository** (or internal equivalent) that every new client app is created from. It ships with:
   - Documented **environment variables** (e.g. `MATT_JAMES_API_URL`, org/app identifiers, auth pattern — exact names TBD when usage/JWT path is finalized).
   - A small **shared bootstrap module** (or future SDK package) used by all apps: load config, attach tenant context, and (once built) emit usage / health checks.
   - **CI** that fails the build if required env vars are missing or a minimal “platform reachability” check does not pass.

2. **You control deploy for staging (and usually production)** — New projects are created under **your** Railway (or chosen host) account so **env vars and webhooks are set by you**. The app cannot ship “unplugged” because the deploy pipeline is the docking step.

**Rule:** New client work = **“New repository from template”** + **deploy from standard pipeline** — never `create-next-app` / blank FastAPI in isolation.

### Option A — Template repo per app (default for isolation)

- One repo per client app, always created from the **same template**.
- Pros: clear client boundaries, separate access, simple mental model.
- Cons: many repos; template updates require a **migration playbook** for old apps.

### Option B — Monorepo (good for in-house delivery)

- Client apps live under e.g. `apps/<client-slug>/` or `deliverables/<client>/` next to `packages/platform-sdk` (or language-specific shared package).
- Pros: one SDK, one CI policy, refactors land everywhere at once.
- Cons: repo size, permission complexity if external collaborators need subset access.

### Option C — Your GitHub org, one repo per client

- Same as A, but repos live under **`mattjames/<client>-app`** (example naming) for brand and access control.
- Still **must** originate from the official template.

### What to avoid

- **Blank starter projects** with no template, no CI guardrails, and env vars pasted only in someone’s notes.
- **Handing off deploy keys** without tying the deployment URL back to **`client_environments`** in the platform registry.

### Checklist when a new app repo exists

Before calling the app “docked”:

- [ ] Org / project / **`app`** row exists in Matt James (or will be created in the same onboarding script).
- [ ] **`client_environments`** rows exist for each URL you care about (preview / staging / production).
- [ ] Repo was created from the **official template** (or monorepo path follows standard layout).
- [ ] Deploy pipeline sets **non-secret** config and injects **secrets** from the host (not committed).
- [ ] (When usage exists) App or gateway reports usage against the same **`organization_id` / `app_id`**.

## Layers to implement (in order)

### Layer A — Control plane (mostly in place)

- Orgs, members, roles, projects, apps
- Client environments (URLs per app)
- Intake, preview builds, approvals, releases
- Admin metering policy CRUD

**Rule:** New features should **read** org/app context from existing models before adding parallel concepts.

### Layer B — Docking contract (define explicitly)

Pick **one primary enforcement surface** (can combine later):

| Pattern | Pros | Cons |
|--------|------|------|
| **MJ-hosted / wrapped deploy** | Strongest guarantee of metering + identity | More ops, you own runtime |
| **Gateway / BFF** in front of client app | Central enforcement without owning full stack | You run edge infra |
| **Mandatory SDK** in app backend | Works with customer-hosted apps | Requires discipline + versioning |

**Deliverable:** A short “Docking spec” section in PRDs: required headers, tenant token shape, which endpoints must be called, failure modes (429 pause, etc.).

### Layer C — Usage plane (build next)

Minimum viable **usage** loop:

1. **Events** — `POST /v1/.../usage-events` (or batch) with `organization_id`, `app_id`, `metric`, `quantity`, `metadata`, timestamp.
2. **Aggregation** — rollups per org/app/period (table or materialized view).
3. **Enforcement** — middleware or service that loads `metering_policies` and rejects/throttles when over cap (respect `is_enforced`, `overage_behavior`).

**Rule:** Metering policy rows are useless until **something** increments usage and **something** checks it on the hot path.

### Layer D — Billing plane (integrate, don’t duplicate)

- Matt James: **entitlements + usage + invoices line-item inputs**
- Payment provider: **cards, tax, dunning**
- Webhooks: sync payment status → org flags (e.g. `paused_for_billing`)

## How to write features from here

1. **Name the tenant slice** — Which `organization_id` / `app_id` does this touch?
2. **Persist, don’t scatter** — Prefer new tables keyed by org/project/app over ad-hoc JSON.
3. **Founder vs client** — Founder Console mutates policy and infra; Client Portal never sees raw keys or metering knobs (`FOUNDERS_CONSOLE_AND_CLIENT_PORTAL_SPEC.md`).
4. **Every new “app capability”** — Ask: *Does this need a usage event?* *Does enforcement run on platform or at gateway?*
5. **Bootstrap path** — When onboarding a client, create org → project → app → environments in one scripted flow (extend `demo/bootstrap` patterns for production onboarding).

## Concrete next milestones (suggested)

1. **Usage events API + storage** + Founder read-only “usage this period” on client profile (spec already mentions usage overview).
2. **Enforcement hook** on one high-value internal route (prove cap/throttle/pause).
3. **Tenant JWT** path for app backends (optional `ENFORCE_TENANT_JWT`) documented as the standard for customer-delivered apps.
4. **Onboarding runbook** — checklist that mirrors “dock” (org, app, env URLs, policy, first usage test).

## Relationship to frozen v1

`V1_OPERATING_FLOW.md` stays the **operational contract** for intake → deploy.  
This document is **Phase 2+ product architecture**: making the container **powered** by usage and billing rails without breaking v1 boundaries.
