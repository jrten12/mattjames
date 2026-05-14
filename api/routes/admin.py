from uuid import UUID

from fastapi import APIRouter, Depends, Header, Request

from api.models.common import ErrorResponse, error_json
from api.models.platform import (
    App,
    AppStatusUpdateRequest,
    Organization,
    Project,
    ProjectResumeRequest,
    ProjectState,
)
from api.routes.dependencies import get_actor, get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.services.platform.repository import NotFoundError, PlatformRepository, TransitionError

router = APIRouter()


@router.get("/admin/orgs/{organization_id}", response_model=Organization, responses={404: {"model": ErrorResponse}})
def admin_get_org(organization_id: UUID, repo: PlatformRepository = Depends(get_repo)):
    try:
        return repo.get_organization(organization_id)
    except NotFoundError:
        return error_json(404, "organization_not_found", "Organization does not exist.")


@router.get("/admin/projects/{project_id}", response_model=Project, responses={404: {"model": ErrorResponse}})
def admin_get_project(project_id: UUID, repo: PlatformRepository = Depends(get_repo)):
    try:
        return repo.get_project(project_id)
    except NotFoundError:
        return error_json(404, "project_not_found", "Project does not exist.")


@router.get("/admin/apps/{app_id}", response_model=App, responses={404: {"model": ErrorResponse}})
def admin_get_app(app_id: UUID, repo: PlatformRepository = Depends(get_repo)):
    try:
        return repo.get_app(app_id)
    except NotFoundError:
        return error_json(404, "app_not_found", "App does not exist.")


@router.post(
    "/admin/apps/{app_id}/status",
    response_model=App,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def admin_update_app_status(
    app_id: UUID,
    body: AppStatusUpdateRequest,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err

    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"admin_app_status:{app_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored

    try:
        updated = repo.update_app_status(app_id, body.status)
    except NotFoundError:
        return error_json(404, "app_not_found", "App does not exist.")

    store_idempotent_result(
        repo,
        operation=f"admin_app_status:{app_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=updated.model_dump(mode="json"),
    )
    return updated


@router.post(
    "/admin/projects/{project_id}/pause",
    response_model=Project,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def admin_pause_project(
    project_id: UUID,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    payload = {"to_state": "paused"}
    restored = restore_if_idempotent(
        repo,
        operation=f"admin_project_pause:{project_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    actor_type, actor_id = get_actor(request)
    try:
        updated = repo.transition_project(
            project_id,
            ProjectState.paused,
            actor_type=actor_type,
            actor_id=actor_id,
            reason_code="admin_pause",
            metadata={"source": "admin_endpoint"},
        )
    except NotFoundError:
        return error_json(404, "project_not_found", "Project does not exist.")
    except TransitionError:
        return error_json(400, "invalid_transition", "Project cannot be paused from current state.")
    store_idempotent_result(
        repo,
        operation=f"admin_project_pause:{project_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=updated.model_dump(mode="json"),
    )
    return updated


@router.post(
    "/admin/projects/{project_id}/resume",
    response_model=Project,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def admin_resume_project(
    project_id: UUID,
    body: ProjectResumeRequest,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"admin_project_resume:{project_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    actor_type, actor_id = get_actor(request)
    try:
        updated = repo.transition_project(
            project_id,
            body.to_state,
            actor_type=actor_type,
            actor_id=actor_id,
            reason_code="admin_resume",
            metadata={"source": "admin_endpoint"},
        )
    except NotFoundError:
        return error_json(404, "project_not_found", "Project does not exist.")
    except TransitionError:
        return error_json(400, "invalid_transition", "Project cannot transition to requested state.")
    store_idempotent_result(
        repo,
        operation=f"admin_project_resume:{project_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=updated.model_dump(mode="json"),
    )
    return updated
