create table if not exists organizations (
  id uuid primary key,
  name text not null,
  slug text unique not null,
  billing_email text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists organization_members (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  user_id text not null,
  role text not null check (role in ('client_owner','client_admin','client_member','internal_pm','internal_lead','finance_ops')),
  created_at timestamptz not null default now(),
  unique (organization_id, user_id)
);

create table if not exists projects (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  name text not null,
  description text,
  current_state text not null check (current_state in (
    'intake','discovery_active','sow_drafting','sow_review',
    'build_in_progress','pilot_live','production_live','expansion','paused','closed'
  )),
  meter_plan_id uuid,
  active_sow_version_id uuid,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_projects_org on projects(organization_id);

create table if not exists apps (
  id uuid primary key,
  project_id uuid not null references projects(id) on delete cascade,
  name text not null,
  slug text not null,
  status text not null check (status in ('draft','active','paused','retired')),
  deploy_mode text not null check (deploy_mode in ('platform_subdomain','custom_domain')),
  platform_subdomain text,
  custom_domain text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (project_id, slug)
);

create index if not exists idx_apps_project on apps(project_id);

create table if not exists intake_requests (
  id uuid primary key,
  organization_id uuid not null references organizations(id) on delete cascade,
  project_id uuid references projects(id) on delete set null,
  request_type text not null check (request_type in ('new_app','update','bugfix','enhancement')),
  title text not null,
  goal text not null,
  details text,
  status text not null check (status in (
    'submitted','triaged','building','preview_ready','client_review',
    'changes_requested','approved','deployed','rejected'
  )),
  owner_user_id text,
  priority text not null default 'normal' check (priority in ('low','normal','high','urgent')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_intake_requests_org on intake_requests(organization_id, created_at);
create index if not exists idx_intake_requests_project on intake_requests(project_id);

create table if not exists preview_builds (
  id uuid primary key,
  intake_request_id uuid not null references intake_requests(id) on delete cascade,
  organization_id uuid not null references organizations(id) on delete cascade,
  project_id uuid references projects(id) on delete set null,
  build_version text not null,
  preview_url text not null,
  status text not null check (status in ('queued','building','ready','failed','expired')),
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_preview_builds_intake on preview_builds(intake_request_id, created_at);
create index if not exists idx_preview_builds_org on preview_builds(organization_id, created_at);

create table if not exists approval_decisions (
  id uuid primary key,
  intake_request_id uuid not null references intake_requests(id) on delete cascade,
  preview_build_id uuid not null references preview_builds(id) on delete cascade,
  organization_id uuid not null references organizations(id) on delete cascade,
  decision text not null check (decision in ('approve','request_changes','reject')),
  comments text,
  decided_by text,
  created_at timestamptz not null default now()
);

create index if not exists idx_approval_decisions_intake on approval_decisions(intake_request_id, created_at);

create table if not exists workflow_events (
  id uuid primary key,
  project_id uuid not null references projects(id) on delete cascade,
  organization_id uuid not null references organizations(id) on delete cascade,
  event_type text not null,
  previous_state text,
  new_state text,
  actor_type text not null check (actor_type in ('client','internal','system','ai')),
  actor_id text,
  reason_code text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_workflow_events_project_created on workflow_events(project_id, created_at);

create table if not exists idempotency_records (
  id uuid primary key,
  key text not null,
  operation text not null,
  request_fingerprint text not null,
  status_code int not null,
  response_json jsonb not null,
  created_at timestamptz not null default now(),
  unique (operation, key)
);
