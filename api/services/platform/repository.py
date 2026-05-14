from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from uuid import UUID, uuid4

from psycopg.types.json import Json

from api.db import get_db_cursor
from api.models.platform import (
    ApprovalDecisionCreate,
    ApprovalDecisionRecord,
    App,
    AppCreate,
    AppStatus,
    IdempotencyRecord,
    IntakeRequest,
    IntakeRequestCreate,
    IntakeRequestStatus,
    IntakeRequestTriageUpdate,
    Organization,
    OrganizationCreate,
    OrganizationMember,
    OrganizationMemberCreate,
    Project,
    ProjectCreate,
    ProjectState,
    PreviewBuild,
    PreviewBuildCreate,
    PreviewBuildStatus,
    PreviewBuildStatusUpdate,
    WorkflowEvent,
)
from api.services.platform.workflow import transition_allowed


class RepositoryError(Exception):
    pass


class NotFoundError(RepositoryError):
    pass


class ConflictError(RepositoryError):
    pass


class TransitionError(RepositoryError):
    pass


class PlatformRepository(ABC):
    @abstractmethod
    def create_organization(self, body: OrganizationCreate) -> Organization: ...

    @abstractmethod
    def list_organizations(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        slug: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[Organization]: ...

    @abstractmethod
    def create_organization_member(
        self,
        organization_id: UUID,
        body: OrganizationMemberCreate,
    ) -> OrganizationMember: ...

    @abstractmethod
    def list_organization_members(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        role: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[OrganizationMember]: ...

    @abstractmethod
    def create_project(self, body: ProjectCreate) -> Project: ...

    @abstractmethod
    def list_projects(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        state: ProjectState | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[Project]: ...

    @abstractmethod
    def create_app(self, body: AppCreate) -> App: ...

    @abstractmethod
    def list_apps(
        self,
        project_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: str | None = None,
        deploy_mode: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[App]: ...

    @abstractmethod
    def create_intake_request(self, body: IntakeRequestCreate) -> IntakeRequest: ...

    @abstractmethod
    def list_intake_requests(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: IntakeRequestStatus | None = None,
        request_type: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[IntakeRequest]: ...

    @abstractmethod
    def update_intake_request_status(self, intake_request_id: UUID, status: IntakeRequestStatus) -> IntakeRequest: ...

    @abstractmethod
    def update_intake_request_triage(
        self,
        intake_request_id: UUID,
        body: IntakeRequestTriageUpdate,
    ) -> IntakeRequest: ...

    @abstractmethod
    def get_intake_request(self, intake_request_id: UUID) -> IntakeRequest: ...

    @abstractmethod
    def create_preview_build(self, body: PreviewBuildCreate) -> PreviewBuild: ...

    @abstractmethod
    def list_preview_builds(
        self,
        intake_request_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: PreviewBuildStatus | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[PreviewBuild]: ...

    @abstractmethod
    def update_preview_build_status(self, preview_build_id: UUID, body: PreviewBuildStatusUpdate) -> PreviewBuild: ...

    @abstractmethod
    def get_preview_build(self, preview_build_id: UUID) -> PreviewBuild: ...

    @abstractmethod
    def create_approval_decision(
        self,
        body: ApprovalDecisionCreate,
        *,
        decided_by: str | None,
    ) -> ApprovalDecisionRecord: ...

    @abstractmethod
    def list_approval_decisions(
        self,
        intake_request_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[ApprovalDecisionRecord]: ...

    @abstractmethod
    def transition_project(
        self,
        project_id: UUID,
        to_state: ProjectState,
        actor_type: str,
        actor_id: str | None,
        reason_code: str,
        metadata: dict,
    ) -> Project: ...

    @abstractmethod
    def list_events(
        self,
        project_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        event_type: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[WorkflowEvent]: ...

    @abstractmethod
    def get_project(self, project_id: UUID) -> Project: ...

    @abstractmethod
    def get_organization(self, organization_id: UUID) -> Organization: ...

    @abstractmethod
    def get_app(self, app_id: UUID) -> App: ...

    @abstractmethod
    def update_app_status(self, app_id: UUID, status: AppStatus) -> App: ...

    @abstractmethod
    def get_idempotency_record(self, operation: str, key: str) -> IdempotencyRecord | None: ...

    @abstractmethod
    def save_idempotency_record(self, record: IdempotencyRecord) -> None: ...


def _now() -> datetime:
    return datetime.now(timezone.utc)


class InMemoryRepository(PlatformRepository):
    def __init__(self) -> None:
        self.organizations: dict[UUID, Organization] = {}
        self.projects: dict[UUID, Project] = {}
        self.apps: dict[UUID, App] = {}
        self.intake_requests: dict[UUID, IntakeRequest] = {}
        self.preview_builds: dict[UUID, PreviewBuild] = {}
        self.approval_decisions: dict[UUID, ApprovalDecisionRecord] = {}
        self.events: list[WorkflowEvent] = []
        self.members: dict[UUID, OrganizationMember] = {}
        self.idempotency: dict[tuple[str, str], IdempotencyRecord] = {}

    def create_organization(self, body: OrganizationCreate) -> Organization:
        if any(item.slug == body.slug for item in self.organizations.values()):
            raise ConflictError("Organization slug already exists.")
        now = _now()
        organization = Organization(
            id=uuid4(),
            name=body.name,
            slug=body.slug,
            billing_email=body.billing_email,
            created_at=now,
            updated_at=now,
        )
        self.organizations[organization.id] = organization
        return organization

    def list_organizations(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        slug: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[Organization]:
        items = sorted(
            self.organizations.values(),
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )
        if slug:
            items = [item for item in items if item.slug == slug]
        if cursor is not None:
            c_time, c_id = cursor
            items = [item for item in items if (item.created_at, item.id) < (c_time, c_id)]
        return items[offset : offset + limit]

    def create_organization_member(
        self,
        organization_id: UUID,
        body: OrganizationMemberCreate,
    ) -> OrganizationMember:
        if organization_id not in self.organizations:
            raise NotFoundError("Organization not found.")
        if any(
            m.organization_id == organization_id and m.user_id == body.user_id
            for m in self.members.values()
        ):
            raise ConflictError("Organization member already exists.")
        member = OrganizationMember(
            id=uuid4(),
            organization_id=organization_id,
            user_id=body.user_id,
            role=body.role,
            created_at=_now(),
        )
        self.members[member.id] = member
        return member

    def list_organization_members(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        role: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[OrganizationMember]:
        items = sorted(
            (m for m in self.members.values() if m.organization_id == organization_id),
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )
        if role:
            items = [m for m in items if m.role == role]
        if cursor is not None:
            c_time, c_id = cursor
            items = [item for item in items if (item.created_at, item.id) < (c_time, c_id)]
        return items[offset : offset + limit]

    def create_project(self, body: ProjectCreate) -> Project:
        if body.organization_id not in self.organizations:
            raise NotFoundError("Organization not found.")
        now = _now()
        project = Project(
            id=uuid4(),
            organization_id=body.organization_id,
            name=body.name,
            description=body.description,
            current_state=ProjectState.intake,
            created_at=now,
            updated_at=now,
        )
        self.projects[project.id] = project
        return project

    def list_projects(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        state: ProjectState | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[Project]:
        items = sorted(
            (p for p in self.projects.values() if p.organization_id == organization_id),
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )
        if state is not None:
            items = [item for item in items if item.current_state == state]
        if cursor is not None:
            c_time, c_id = cursor
            items = [item for item in items if (item.created_at, item.id) < (c_time, c_id)]
        return items[offset : offset + limit]

    def create_app(self, body: AppCreate) -> App:
        project = self.projects.get(body.project_id)
        if project is None:
            raise NotFoundError("Project not found.")
        if any(item.project_id == body.project_id and item.slug == body.slug for item in self.apps.values()):
            raise ConflictError("App slug already exists for this project.")
        now = _now()
        app = App(
            id=uuid4(),
            project_id=body.project_id,
            name=body.name,
            slug=body.slug,
            status="draft",
            deploy_mode=body.deploy_mode,
            platform_subdomain=body.platform_subdomain,
            custom_domain=body.custom_domain,
            created_at=now,
            updated_at=now,
        )
        self.apps[app.id] = app
        self._append_event(project, None, None, "app_created", "internal", None, "app_create", {"app_id": str(app.id)})
        return app

    def list_apps(
        self,
        project_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: str | None = None,
        deploy_mode: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[App]:
        items = sorted(
            (a for a in self.apps.values() if a.project_id == project_id),
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )
        if status is not None:
            items = [item for item in items if item.status == status]
        if deploy_mode is not None:
            items = [item for item in items if item.deploy_mode == deploy_mode]
        if cursor is not None:
            c_time, c_id = cursor
            items = [item for item in items if (item.created_at, item.id) < (c_time, c_id)]
        return items[offset : offset + limit]

    def create_intake_request(self, body: IntakeRequestCreate) -> IntakeRequest:
        if body.organization_id not in self.organizations:
            raise NotFoundError("Organization not found.")
        if body.project_id is not None:
            project = self.projects.get(body.project_id)
            if project is None:
                raise NotFoundError("Project not found.")
            if project.organization_id != body.organization_id:
                raise ConflictError("Project does not belong to organization.")
        now = _now()
        intake_request = IntakeRequest(
            id=uuid4(),
            organization_id=body.organization_id,
            project_id=body.project_id,
            request_type=body.request_type,
            title=body.title,
            goal=body.goal,
            details=body.details,
            status=IntakeRequestStatus.submitted,
            owner_user_id=None,
            priority="normal",
            created_at=now,
            updated_at=now,
        )
        self.intake_requests[intake_request.id] = intake_request
        return intake_request

    def list_intake_requests(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: IntakeRequestStatus | None = None,
        request_type: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[IntakeRequest]:
        items = sorted(
            (i for i in self.intake_requests.values() if i.organization_id == organization_id),
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )
        if status is not None:
            items = [item for item in items if item.status == status]
        if request_type is not None:
            items = [item for item in items if item.request_type == request_type]
        if cursor is not None:
            c_time, c_id = cursor
            items = [item for item in items if (item.created_at, item.id) < (c_time, c_id)]
        return items[offset : offset + limit]

    def update_intake_request_status(self, intake_request_id: UUID, status: IntakeRequestStatus) -> IntakeRequest:
        intake_request = self.get_intake_request(intake_request_id)
        updated = intake_request.model_copy(update={"status": status, "updated_at": _now()})
        self.intake_requests[intake_request_id] = updated
        return updated

    def update_intake_request_triage(
        self,
        intake_request_id: UUID,
        body: IntakeRequestTriageUpdate,
    ) -> IntakeRequest:
        intake_request = self.get_intake_request(intake_request_id)
        updated = intake_request.model_copy(
            update={
                "owner_user_id": body.owner_user_id,
                "priority": body.priority,
                "updated_at": _now(),
            }
        )
        self.intake_requests[intake_request_id] = updated
        return updated

    def get_intake_request(self, intake_request_id: UUID) -> IntakeRequest:
        intake_request = self.intake_requests.get(intake_request_id)
        if intake_request is None:
            raise NotFoundError("Intake request not found.")
        return intake_request

    def create_preview_build(self, body: PreviewBuildCreate) -> PreviewBuild:
        intake_request = self.get_intake_request(body.intake_request_id)
        now = _now()
        preview_build = PreviewBuild(
            id=uuid4(),
            intake_request_id=body.intake_request_id,
            organization_id=intake_request.organization_id,
            project_id=intake_request.project_id,
            build_version=body.build_version,
            preview_url=body.preview_url,
            status=PreviewBuildStatus.queued,
            notes=body.notes,
            created_at=now,
            updated_at=now,
        )
        self.preview_builds[preview_build.id] = preview_build
        return preview_build

    def list_preview_builds(
        self,
        intake_request_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: PreviewBuildStatus | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[PreviewBuild]:
        items = sorted(
            (b for b in self.preview_builds.values() if b.intake_request_id == intake_request_id),
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )
        if status is not None:
            items = [item for item in items if item.status == status]
        if cursor is not None:
            c_time, c_id = cursor
            items = [item for item in items if (item.created_at, item.id) < (c_time, c_id)]
        return items[offset : offset + limit]

    def update_preview_build_status(self, preview_build_id: UUID, body: PreviewBuildStatusUpdate) -> PreviewBuild:
        preview_build = self.get_preview_build(preview_build_id)
        updated = preview_build.model_copy(update={"status": body.status, "updated_at": _now()})
        self.preview_builds[preview_build_id] = updated
        return updated

    def get_preview_build(self, preview_build_id: UUID) -> PreviewBuild:
        preview_build = self.preview_builds.get(preview_build_id)
        if preview_build is None:
            raise NotFoundError("Preview build not found.")
        return preview_build

    def create_approval_decision(
        self,
        body: ApprovalDecisionCreate,
        *,
        decided_by: str | None,
    ) -> ApprovalDecisionRecord:
        intake_request = self.get_intake_request(body.intake_request_id)
        preview_build = self.get_preview_build(body.preview_build_id)
        if preview_build.intake_request_id != body.intake_request_id:
            raise ConflictError("Preview build does not belong to intake request.")
        decision = ApprovalDecisionRecord(
            id=uuid4(),
            intake_request_id=body.intake_request_id,
            preview_build_id=body.preview_build_id,
            organization_id=intake_request.organization_id,
            decision=body.decision,
            comments=body.comments,
            decided_by=decided_by,
            created_at=_now(),
        )
        self.approval_decisions[decision.id] = decision
        status_map = {
            "approve": IntakeRequestStatus.approved,
            "request_changes": IntakeRequestStatus.changes_requested,
            "reject": IntakeRequestStatus.rejected,
        }
        self.update_intake_request_status(body.intake_request_id, status_map[body.decision.value])
        return decision

    def list_approval_decisions(
        self,
        intake_request_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[ApprovalDecisionRecord]:
        items = sorted(
            (d for d in self.approval_decisions.values() if d.intake_request_id == intake_request_id),
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        )
        if cursor is not None:
            c_time, c_id = cursor
            items = [item for item in items if (item.created_at, item.id) < (c_time, c_id)]
        return items[offset : offset + limit]

    def get_project(self, project_id: UUID) -> Project:
        project = self.projects.get(project_id)
        if project is None:
            raise NotFoundError("Project not found.")
        return project

    def get_organization(self, organization_id: UUID) -> Organization:
        organization = self.organizations.get(organization_id)
        if organization is None:
            raise NotFoundError("Organization not found.")
        return organization

    def get_app(self, app_id: UUID) -> App:
        app = self.apps.get(app_id)
        if app is None:
            raise NotFoundError("App not found.")
        return app

    def update_app_status(self, app_id: UUID, status: AppStatus) -> App:
        app = self.get_app(app_id)
        updated = app.model_copy(update={"status": status.value, "updated_at": _now()})
        self.apps[app_id] = updated
        return updated

    def transition_project(
        self,
        project_id: UUID,
        to_state: ProjectState,
        actor_type: str,
        actor_id: str | None,
        reason_code: str,
        metadata: dict,
    ) -> Project:
        current = self.get_project(project_id)
        if not transition_allowed(current.current_state, to_state):
            raise TransitionError("Transition is not allowed.")
        updated = current.model_copy(update={"current_state": to_state, "updated_at": _now()})
        self.projects[project_id] = updated
        self._append_event(
            updated,
            current.current_state,
            to_state,
            "state_transitioned",
            actor_type,
            actor_id,
            reason_code,
            metadata,
        )
        return updated

    def _append_event(
        self,
        project: Project,
        previous_state: ProjectState | None,
        new_state: ProjectState | None,
        event_type: str,
        actor_type: str,
        actor_id: str | None,
        reason_code: str | None,
        metadata: dict,
    ) -> None:
        self.events.append(
            WorkflowEvent(
                id=uuid4(),
                project_id=project.id,
                organization_id=project.organization_id,
                event_type=event_type,
                previous_state=previous_state,
                new_state=new_state,
                actor_type=actor_type,
                actor_id=actor_id,
                reason_code=reason_code,
                metadata=metadata,
                created_at=_now(),
            )
        )

    def list_events(
        self,
        project_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        event_type: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[WorkflowEvent]:
        items = sorted(
            (event for event in self.events if event.project_id == project_id),
            key=lambda item: (item.created_at, item.id),
        )
        if event_type:
            items = [event for event in items if event.event_type == event_type]
        if cursor is not None:
            c_time, c_id = cursor
            items = [item for item in items if (item.created_at, item.id) > (c_time, c_id)]
        return items[offset : offset + limit]

    def get_idempotency_record(self, operation: str, key: str) -> IdempotencyRecord | None:
        return self.idempotency.get((operation, key))

    def save_idempotency_record(self, record: IdempotencyRecord) -> None:
        self.idempotency[(record.operation, record.key)] = record


class PostgresRepository(PlatformRepository):
    def create_organization(self, body: OrganizationCreate) -> Organization:
        with get_db_cursor() as cur:
            try:
                cur.execute(
                    """
                    insert into organizations(id, name, slug, billing_email)
                    values(%s, %s, %s, %s)
                    returning id, name, slug, billing_email, created_at, updated_at
                    """,
                    (uuid4(), body.name, body.slug, body.billing_email),
                )
            except Exception as exc:
                raise ConflictError("Organization create failed.") from exc
            row = cur.fetchone()
            return Organization(**row)

    def list_organizations(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        slug: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[Organization]:
        with get_db_cursor() as cur:
            if slug is not None and cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, name, slug, billing_email, created_at, updated_at
                    from organizations
                    where slug = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (slug, c_time, c_id, limit, offset),
                )
            elif slug is not None:
                cur.execute(
                    """
                    select id, name, slug, billing_email, created_at, updated_at
                    from organizations
                    where slug = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (slug, limit, offset),
                )
            elif cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, name, slug, billing_email, created_at, updated_at
                    from organizations
                    where (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (c_time, c_id, limit, offset),
                )
            else:
                cur.execute(
                    """
                    select id, name, slug, billing_email, created_at, updated_at
                    from organizations
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (limit, offset),
                )
            return [Organization(**row) for row in cur.fetchall()]

    def create_organization_member(
        self,
        organization_id: UUID,
        body: OrganizationMemberCreate,
    ) -> OrganizationMember:
        with get_db_cursor() as cur:
            cur.execute("select id from organizations where id = %s", (organization_id,))
            if cur.fetchone() is None:
                raise NotFoundError("Organization not found.")
            try:
                cur.execute(
                    """
                    insert into organization_members(id, organization_id, user_id, role)
                    values(%s, %s, %s, %s)
                    returning id, organization_id, user_id, role, created_at
                    """,
                    (uuid4(), organization_id, body.user_id, body.role),
                )
            except Exception as exc:
                raise ConflictError("Organization member create failed.") from exc
            return OrganizationMember(**cur.fetchone())

    def list_organization_members(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        role: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[OrganizationMember]:
        with get_db_cursor() as cur:
            if role is not None and cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, organization_id, user_id, role, created_at
                    from organization_members
                    where organization_id = %s and role = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (organization_id, role, c_time, c_id, limit, offset),
                )
            elif role is not None:
                cur.execute(
                    """
                    select id, organization_id, user_id, role, created_at
                    from organization_members
                    where organization_id = %s and role = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (organization_id, role, limit, offset),
                )
            elif cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, organization_id, user_id, role, created_at
                    from organization_members
                    where organization_id = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (organization_id, c_time, c_id, limit, offset),
                )
            else:
                cur.execute(
                    """
                    select id, organization_id, user_id, role, created_at
                    from organization_members
                    where organization_id = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (organization_id, limit, offset),
                )
            return [OrganizationMember(**row) for row in cur.fetchall()]

    def create_project(self, body: ProjectCreate) -> Project:
        with get_db_cursor() as cur:
            cur.execute("select id from organizations where id = %s", (body.organization_id,))
            if cur.fetchone() is None:
                raise NotFoundError("Organization not found.")
            cur.execute(
                """
                insert into projects(id, organization_id, name, description, current_state)
                values(%s, %s, %s, %s, %s)
                returning id, organization_id, name, description, current_state, created_at, updated_at
                """,
                (uuid4(), body.organization_id, body.name, body.description, ProjectState.intake.value),
            )
            row = cur.fetchone()
            return Project(**row)

    def list_projects(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        state: ProjectState | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[Project]:
        with get_db_cursor() as cur:
            if state is not None and cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, organization_id, name, description, current_state, created_at, updated_at
                    from projects
                    where organization_id = %s and current_state = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (organization_id, state.value, c_time, c_id, limit, offset),
                )
            elif state is not None:
                cur.execute(
                    """
                    select id, organization_id, name, description, current_state, created_at, updated_at
                    from projects
                    where organization_id = %s and current_state = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (organization_id, state.value, limit, offset),
                )
            elif cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, organization_id, name, description, current_state, created_at, updated_at
                    from projects
                    where organization_id = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (organization_id, c_time, c_id, limit, offset),
                )
            else:
                cur.execute(
                    """
                    select id, organization_id, name, description, current_state, created_at, updated_at
                    from projects
                    where organization_id = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (organization_id, limit, offset),
                )
            return [Project(**row) for row in cur.fetchall()]

    def create_app(self, body: AppCreate) -> App:
        with get_db_cursor() as cur:
            cur.execute("select id from projects where id = %s", (body.project_id,))
            if cur.fetchone() is None:
                raise NotFoundError("Project not found.")
            try:
                cur.execute(
                    """
                    insert into apps(
                        id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain
                    )
                    values(%s, %s, %s, %s, %s, %s, %s, %s)
                    returning id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    """,
                    (
                        uuid4(),
                        body.project_id,
                        body.name,
                        body.slug,
                        "draft",
                        body.deploy_mode,
                        body.platform_subdomain,
                        body.custom_domain,
                    ),
                )
            except Exception as exc:
                raise ConflictError("App create failed.") from exc
            row = cur.fetchone()
            return App(**row)

    def list_apps(
        self,
        project_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: str | None = None,
        deploy_mode: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[App]:
        with get_db_cursor() as cur:
            if status is not None and deploy_mode is not None and cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    from apps
                    where project_id = %s and status = %s and deploy_mode = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (project_id, status, deploy_mode, c_time, c_id, limit, offset),
                )
            elif status is not None and deploy_mode is not None:
                cur.execute(
                    """
                    select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    from apps
                    where project_id = %s and status = %s and deploy_mode = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (project_id, status, deploy_mode, limit, offset),
                )
            elif status is not None and cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    from apps
                    where project_id = %s and status = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (project_id, status, c_time, c_id, limit, offset),
                )
            elif status is not None:
                cur.execute(
                    """
                    select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    from apps
                    where project_id = %s and status = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (project_id, status, limit, offset),
                )
            elif deploy_mode is not None and cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    from apps
                    where project_id = %s and deploy_mode = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (project_id, deploy_mode, c_time, c_id, limit, offset),
                )
            elif deploy_mode is not None:
                cur.execute(
                    """
                    select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    from apps
                    where project_id = %s and deploy_mode = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (project_id, deploy_mode, limit, offset),
                )
            elif cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    from apps
                    where project_id = %s and (created_at, id) < (%s, %s)
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (project_id, c_time, c_id, limit, offset),
                )
            else:
                cur.execute(
                    """
                    select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                    from apps
                    where project_id = %s
                    order by created_at desc, id desc
                    limit %s offset %s
                    """,
                    (project_id, limit, offset),
                )
            return [App(**row) for row in cur.fetchall()]

    def create_intake_request(self, body: IntakeRequestCreate) -> IntakeRequest:
        with get_db_cursor() as cur:
            cur.execute("select id from organizations where id = %s", (body.organization_id,))
            if cur.fetchone() is None:
                raise NotFoundError("Organization not found.")
            if body.project_id is not None:
                cur.execute(
                    "select id from projects where id = %s and organization_id = %s",
                    (body.project_id, body.organization_id),
                )
                if cur.fetchone() is None:
                    raise ConflictError("Project does not belong to organization.")
            cur.execute(
                """
                insert into intake_requests(
                    id, organization_id, project_id, request_type, title, goal, details, status, owner_user_id, priority
                ) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                returning id, organization_id, project_id, request_type, title, goal, details, status, owner_user_id, priority, created_at, updated_at
                """,
                (
                    uuid4(),
                    body.organization_id,
                    body.project_id,
                    body.request_type,
                    body.title,
                    body.goal,
                    body.details,
                    IntakeRequestStatus.submitted.value,
                    None,
                    "normal",
                ),
            )
            row = cur.fetchone()
            return IntakeRequest(**row)

    def list_intake_requests(
        self,
        organization_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: IntakeRequestStatus | None = None,
        request_type: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[IntakeRequest]:
        with get_db_cursor() as cur:
            query = """
                select id, organization_id, project_id, request_type, title, goal, details, status, owner_user_id, priority, created_at, updated_at
                from intake_requests
                where organization_id = %s
            """
            params: list = [organization_id]
            if status is not None:
                query += " and status = %s"
                params.append(status.value)
            if request_type is not None:
                query += " and request_type = %s"
                params.append(request_type)
            if cursor is not None:
                c_time, c_id = cursor
                query += " and (created_at, id) < (%s, %s)"
                params.extend([c_time, c_id])
            query += " order by created_at desc, id desc limit %s offset %s"
            params.extend([limit, offset])
            cur.execute(query, tuple(params))
            return [IntakeRequest(**row) for row in cur.fetchall()]

    def update_intake_request_status(self, intake_request_id: UUID, status: IntakeRequestStatus) -> IntakeRequest:
        with get_db_cursor() as cur:
            cur.execute(
                """
                update intake_requests
                set status = %s, updated_at = now()
                where id = %s
                returning id, organization_id, project_id, request_type, title, goal, details, status, owner_user_id, priority, created_at, updated_at
                """,
                (status.value, intake_request_id),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("Intake request not found.")
            return IntakeRequest(**row)

    def update_intake_request_triage(
        self,
        intake_request_id: UUID,
        body: IntakeRequestTriageUpdate,
    ) -> IntakeRequest:
        with get_db_cursor() as cur:
            cur.execute(
                """
                update intake_requests
                set owner_user_id = %s, priority = %s, updated_at = now()
                where id = %s
                returning id, organization_id, project_id, request_type, title, goal, details, status, owner_user_id, priority, created_at, updated_at
                """,
                (body.owner_user_id, body.priority, intake_request_id),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("Intake request not found.")
            return IntakeRequest(**row)

    def get_intake_request(self, intake_request_id: UUID) -> IntakeRequest:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select id, organization_id, project_id, request_type, title, goal, details, status, owner_user_id, priority, created_at, updated_at
                from intake_requests
                where id = %s
                """,
                (intake_request_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("Intake request not found.")
            return IntakeRequest(**row)

    def create_preview_build(self, body: PreviewBuildCreate) -> PreviewBuild:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select id, organization_id, project_id
                from intake_requests
                where id = %s
                """,
                (body.intake_request_id,),
            )
            intake_row = cur.fetchone()
            if intake_row is None:
                raise NotFoundError("Intake request not found.")
            cur.execute(
                """
                insert into preview_builds(
                    id, intake_request_id, organization_id, project_id, build_version, preview_url, status, notes
                ) values(%s, %s, %s, %s, %s, %s, %s, %s)
                returning id, intake_request_id, organization_id, project_id, build_version, preview_url, status, notes, created_at, updated_at
                """,
                (
                    uuid4(),
                    body.intake_request_id,
                    intake_row["organization_id"],
                    intake_row["project_id"],
                    body.build_version,
                    body.preview_url,
                    PreviewBuildStatus.queued.value,
                    body.notes,
                ),
            )
            row = cur.fetchone()
            return PreviewBuild(**row)

    def list_preview_builds(
        self,
        intake_request_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        status: PreviewBuildStatus | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[PreviewBuild]:
        with get_db_cursor() as cur:
            query = """
                select id, intake_request_id, organization_id, project_id, build_version, preview_url, status, notes, created_at, updated_at
                from preview_builds
                where intake_request_id = %s
            """
            params: list = [intake_request_id]
            if status is not None:
                query += " and status = %s"
                params.append(status.value)
            if cursor is not None:
                c_time, c_id = cursor
                query += " and (created_at, id) < (%s, %s)"
                params.extend([c_time, c_id])
            query += " order by created_at desc, id desc limit %s offset %s"
            params.extend([limit, offset])
            cur.execute(query, tuple(params))
            return [PreviewBuild(**row) for row in cur.fetchall()]

    def update_preview_build_status(self, preview_build_id: UUID, body: PreviewBuildStatusUpdate) -> PreviewBuild:
        with get_db_cursor() as cur:
            cur.execute(
                """
                update preview_builds
                set status = %s, updated_at = now()
                where id = %s
                returning id, intake_request_id, organization_id, project_id, build_version, preview_url, status, notes, created_at, updated_at
                """,
                (body.status.value, preview_build_id),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("Preview build not found.")
            return PreviewBuild(**row)

    def get_preview_build(self, preview_build_id: UUID) -> PreviewBuild:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select id, intake_request_id, organization_id, project_id, build_version, preview_url, status, notes, created_at, updated_at
                from preview_builds
                where id = %s
                """,
                (preview_build_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("Preview build not found.")
            return PreviewBuild(**row)

    def create_approval_decision(
        self,
        body: ApprovalDecisionCreate,
        *,
        decided_by: str | None,
    ) -> ApprovalDecisionRecord:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select id, organization_id
                from intake_requests
                where id = %s
                for update
                """,
                (body.intake_request_id,),
            )
            intake_row = cur.fetchone()
            if intake_row is None:
                raise NotFoundError("Intake request not found.")
            cur.execute(
                """
                select id, intake_request_id
                from preview_builds
                where id = %s
                """,
                (body.preview_build_id,),
            )
            preview_row = cur.fetchone()
            if preview_row is None:
                raise NotFoundError("Preview build not found.")
            if preview_row["intake_request_id"] != body.intake_request_id:
                raise ConflictError("Preview build does not belong to intake request.")

            cur.execute(
                """
                insert into approval_decisions(
                    id, intake_request_id, preview_build_id, organization_id, decision, comments, decided_by
                ) values(%s, %s, %s, %s, %s, %s, %s)
                returning id, intake_request_id, preview_build_id, organization_id, decision, comments, decided_by, created_at
                """,
                (
                    uuid4(),
                    body.intake_request_id,
                    body.preview_build_id,
                    intake_row["organization_id"],
                    body.decision.value,
                    body.comments,
                    decided_by,
                ),
            )
            decision = ApprovalDecisionRecord(**cur.fetchone())
            status_map = {
                "approve": IntakeRequestStatus.approved.value,
                "request_changes": IntakeRequestStatus.changes_requested.value,
                "reject": IntakeRequestStatus.rejected.value,
            }
            cur.execute(
                """
                update intake_requests
                set status = %s, updated_at = now()
                where id = %s
                """,
                (status_map[body.decision.value], body.intake_request_id),
            )
            return decision

    def list_approval_decisions(
        self,
        intake_request_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[ApprovalDecisionRecord]:
        with get_db_cursor() as cur:
            query = """
                select id, intake_request_id, preview_build_id, organization_id, decision, comments, decided_by, created_at
                from approval_decisions
                where intake_request_id = %s
            """
            params: list = [intake_request_id]
            if cursor is not None:
                c_time, c_id = cursor
                query += " and (created_at, id) < (%s, %s)"
                params.extend([c_time, c_id])
            query += " order by created_at desc, id desc limit %s offset %s"
            params.extend([limit, offset])
            cur.execute(query, tuple(params))
            return [ApprovalDecisionRecord(**row) for row in cur.fetchall()]

    def get_project(self, project_id: UUID) -> Project:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select id, organization_id, name, description, current_state, created_at, updated_at
                from projects
                where id = %s
                """,
                (project_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("Project not found.")
            return Project(**row)

    def get_organization(self, organization_id: UUID) -> Organization:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select id, name, slug, billing_email, created_at, updated_at
                from organizations
                where id = %s
                """,
                (organization_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("Organization not found.")
            return Organization(**row)

    def get_app(self, app_id: UUID) -> App:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                from apps
                where id = %s
                """,
                (app_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("App not found.")
            return App(**row)

    def update_app_status(self, app_id: UUID, status: AppStatus) -> App:
        with get_db_cursor() as cur:
            cur.execute(
                """
                update apps
                set status = %s, updated_at = now()
                where id = %s
                returning id, project_id, name, slug, status, deploy_mode, platform_subdomain, custom_domain, created_at, updated_at
                """,
                (status.value, app_id),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("App not found.")
            return App(**row)

    def transition_project(
        self,
        project_id: UUID,
        to_state: ProjectState,
        actor_type: str,
        actor_id: str | None,
        reason_code: str,
        metadata: dict,
    ) -> Project:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select id, organization_id, name, description, current_state, created_at, updated_at
                from projects
                where id = %s
                for update
                """,
                (project_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise NotFoundError("Project not found.")
            current = Project(**row)
            if not transition_allowed(current.current_state, to_state):
                raise TransitionError("Transition is not allowed.")

            cur.execute(
                """
                update projects
                set current_state = %s, updated_at = now()
                where id = %s
                returning id, organization_id, name, description, current_state, created_at, updated_at
                """,
                (to_state.value, project_id),
            )
            updated = Project(**cur.fetchone())
            cur.execute(
                """
                insert into workflow_events(
                    id, project_id, organization_id, event_type, previous_state, new_state,
                    actor_type, actor_id, reason_code, metadata
                ) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    uuid4(),
                    project_id,
                    updated.organization_id,
                    "state_transitioned",
                    current.current_state.value,
                    to_state.value,
                    actor_type,
                    actor_id,
                    reason_code,
                    Json(metadata),
                ),
            )
            return updated

    def list_events(
        self,
        project_id: UUID,
        *,
        limit: int = 50,
        offset: int = 0,
        event_type: str | None = None,
        cursor: tuple[datetime, UUID] | None = None,
    ) -> list[WorkflowEvent]:
        with get_db_cursor() as cur:
            if event_type is not None and cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, project_id, organization_id, event_type, previous_state, new_state,
                           actor_type, actor_id, reason_code, metadata, created_at
                    from workflow_events
                    where project_id = %s and event_type = %s and (created_at, id) > (%s, %s)
                    order by created_at asc, id asc
                    limit %s offset %s
                    """,
                    (project_id, event_type, c_time, c_id, limit, offset),
                )
            elif event_type is not None:
                cur.execute(
                    """
                    select id, project_id, organization_id, event_type, previous_state, new_state,
                           actor_type, actor_id, reason_code, metadata, created_at
                    from workflow_events
                    where project_id = %s and event_type = %s
                    order by created_at asc, id asc
                    limit %s offset %s
                    """,
                    (project_id, event_type, limit, offset),
                )
            elif cursor is not None:
                c_time, c_id = cursor
                cur.execute(
                    """
                    select id, project_id, organization_id, event_type, previous_state, new_state,
                           actor_type, actor_id, reason_code, metadata, created_at
                    from workflow_events
                    where project_id = %s and (created_at, id) > (%s, %s)
                    order by created_at asc, id asc
                    limit %s offset %s
                    """,
                    (project_id, c_time, c_id, limit, offset),
                )
            else:
                cur.execute(
                    """
                    select id, project_id, organization_id, event_type, previous_state, new_state,
                           actor_type, actor_id, reason_code, metadata, created_at
                    from workflow_events
                    where project_id = %s
                    order by created_at asc, id asc
                    limit %s offset %s
                    """,
                    (project_id, limit, offset),
                )
            rows = cur.fetchall()
            normalized = []
            for row in rows:
                metadata = row["metadata"]
                if isinstance(metadata, str):
                    metadata = json.loads(metadata)
                row["metadata"] = metadata
                normalized.append(WorkflowEvent(**row))
            return normalized

    def get_idempotency_record(self, operation: str, key: str) -> IdempotencyRecord | None:
        with get_db_cursor() as cur:
            cur.execute(
                """
                select key, operation, request_fingerprint, status_code, response_json
                from idempotency_records
                where operation = %s and key = %s
                """,
                (operation, key),
            )
            row = cur.fetchone()
            if row is None:
                return None
            response_json = row["response_json"]
            if isinstance(response_json, str):
                response_json = json.loads(response_json)
            row["response_json"] = response_json
            return IdempotencyRecord(**row)

    def save_idempotency_record(self, record: IdempotencyRecord) -> None:
        with get_db_cursor() as cur:
            cur.execute(
                """
                insert into idempotency_records(id, key, operation, request_fingerprint, status_code, response_json)
                values(%s, %s, %s, %s, %s, %s)
                on conflict (operation, key) do nothing
                """,
                (
                    uuid4(),
                    record.key,
                    record.operation,
                    record.request_fingerprint,
                    record.status_code,
                    Json(record.response_json),
                ),
            )
