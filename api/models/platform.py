from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectState(str, Enum):
    intake = "intake"
    discovery_active = "discovery_active"
    sow_drafting = "sow_drafting"
    sow_review = "sow_review"
    build_in_progress = "build_in_progress"
    pilot_live = "pilot_live"
    production_live = "production_live"
    expansion = "expansion"
    paused = "paused"
    closed = "closed"


class OrganizationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=2, max_length=120)
    billing_email: str | None = None


class Organization(BaseModel):
    id: UUID
    name: str
    slug: str
    billing_email: str | None
    created_at: datetime
    updated_at: datetime


class OrganizationMemberCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    user_id: str = Field(min_length=1, max_length=200)
    role: str = Field(
        pattern="^(client_owner|client_admin|client_member|internal_pm|internal_lead|finance_ops)$"
    )


class OrganizationMember(BaseModel):
    id: UUID
    organization_id: UUID
    user_id: str
    role: str
    created_at: datetime


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    organization_id: UUID
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=3000)


class Project(BaseModel):
    id: UUID
    organization_id: UUID
    name: str
    description: str | None
    current_state: ProjectState
    created_at: datetime
    updated_at: datetime


class AppCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_id: UUID
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=2, max_length=120)
    deploy_mode: str = Field(pattern="^(platform_subdomain|custom_domain)$")
    platform_subdomain: str | None = None
    custom_domain: str | None = None


class App(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    slug: str
    status: str
    deploy_mode: str
    platform_subdomain: str | None
    custom_domain: str | None
    created_at: datetime
    updated_at: datetime


class AppStatus(str, Enum):
    draft = "draft"
    active = "active"
    paused = "paused"
    retired = "retired"


class IntakeRequestStatus(str, Enum):
    submitted = "submitted"
    triaged = "triaged"
    building = "building"
    preview_ready = "preview_ready"
    client_review = "client_review"
    changes_requested = "changes_requested"
    approved = "approved"
    deployed = "deployed"
    rejected = "rejected"


class IntakeRequestCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    organization_id: UUID
    project_id: UUID | None = None
    request_type: str = Field(pattern="^(new_app|update|bugfix|enhancement)$")
    title: str = Field(min_length=2, max_length=200)
    goal: str = Field(min_length=2, max_length=2000)
    details: str | None = Field(default=None, max_length=8000)


class IntakeRequestStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: IntakeRequestStatus


class IntakeRequest(BaseModel):
    id: UUID
    organization_id: UUID
    project_id: UUID | None
    request_type: str
    title: str
    goal: str
    details: str | None
    status: IntakeRequestStatus
    owner_user_id: str | None
    priority: str
    created_at: datetime
    updated_at: datetime


class IntakeRequestTriageUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    owner_user_id: str | None = Field(default=None, max_length=200)
    priority: str = Field(pattern="^(low|normal|high|urgent)$")


class PreviewBuildStatus(str, Enum):
    queued = "queued"
    building = "building"
    ready = "ready"
    failed = "failed"
    expired = "expired"


class PreviewBuildCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    intake_request_id: UUID
    build_version: str = Field(min_length=1, max_length=120)
    preview_url: str = Field(min_length=8, max_length=400)
    notes: str | None = Field(default=None, max_length=4000)


class PreviewBuildStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: PreviewBuildStatus


class PreviewBuild(BaseModel):
    id: UUID
    intake_request_id: UUID
    organization_id: UUID
    project_id: UUID | None
    build_version: str
    preview_url: str
    status: PreviewBuildStatus
    notes: str | None
    created_at: datetime
    updated_at: datetime


class ApprovalDecision(str, Enum):
    approve = "approve"
    request_changes = "request_changes"
    reject = "reject"


class ApprovalDecisionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    intake_request_id: UUID
    preview_build_id: UUID
    decision: ApprovalDecision
    comments: str | None = Field(default=None, max_length=4000)


class ApprovalDecisionRecord(BaseModel):
    id: UUID
    intake_request_id: UUID
    preview_build_id: UUID
    organization_id: UUID
    decision: ApprovalDecision
    comments: str | None
    decided_by: str | None
    created_at: datetime


class TransitionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    to_state: ProjectState
    reason_code: str = Field(min_length=1, max_length=120)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowEvent(BaseModel):
    id: UUID
    project_id: UUID
    organization_id: UUID
    event_type: str
    previous_state: ProjectState | None
    new_state: ProjectState | None
    actor_type: str
    actor_id: str | None
    reason_code: str | None
    metadata: dict[str, Any]
    created_at: datetime


class IdempotencyRecord(BaseModel):
    key: str
    operation: str
    request_fingerprint: str
    status_code: int
    response_json: dict[str, Any]


class AppStatusUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: AppStatus


class ProjectResumeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    to_state: ProjectState = ProjectState.discovery_active


class DemoBootstrapRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    org_name: str = Field(default="Demo Health Group", min_length=2, max_length=200)
    org_slug: str = Field(default="demo-health-group", min_length=2, max_length=120)
    owner_user_id: str = Field(default="demo_owner", min_length=1, max_length=200)
    project_name: str = Field(default="Patient Intake Assistant", min_length=2, max_length=200)
    app_name: str = Field(default="Intake Copilot", min_length=2, max_length=200)
    app_slug: str = Field(default="intake-copilot", min_length=2, max_length=120)


class DemoBootstrapResponse(BaseModel):
    organization: Organization
    owner_member: OrganizationMember
    project: Project
    app: App
