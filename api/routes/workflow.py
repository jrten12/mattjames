from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response

from api.models.common import ErrorResponse, error_json
from api.models.platform import Project, TransitionRequest, WorkflowEvent
from api.pagination import decode_cursor, encode_cursor
from api.routes.dependencies import get_actor, get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.routes.scope import enforce_org_scope
from api.services.platform.repository import NotFoundError, PlatformRepository, TransitionError

router = APIRouter()


@router.post(
    "/projects/{project_id}/transitions",
    response_model=Project,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def transition_project(
    project_id: UUID,
    body: TransitionRequest,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    try:
        project = repo.get_project(project_id)
    except NotFoundError:
        return error_json(404, "project_not_found", "Project does not exist.")

    scope_err = enforce_org_scope(request, project.organization_id)
    if scope_err is not None:
        return scope_err

    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"transition_project:{project_id}",
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
            reason_code=body.reason_code,
            metadata=body.metadata,
        )
        store_idempotent_result(
            repo,
            operation=f"transition_project:{project_id}",
            key=idempotency_key,
            payload=payload,
            status_code=200,
            response_json=updated.model_dump(mode="json"),
        )
        return updated
    except TransitionError:
        return error_json(400, "invalid_transition", "Transition is not allowed.")


@router.get(
    "/projects/{project_id}/events",
    response_model=list[WorkflowEvent],
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def list_events(
    project_id: UUID,
    request: Request,
    response: Response,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    event_type: str | None = Query(default=None),
    cursor: str | None = Query(default=None),
    repo: PlatformRepository = Depends(get_repo),
):
    try:
        project = repo.get_project(project_id)
    except NotFoundError:
        return error_json(404, "project_not_found", "Project does not exist.")
    scope_err = enforce_org_scope(request, project.organization_id)
    if scope_err is not None:
        return scope_err
    parsed = decode_cursor(cursor) if cursor else None
    if cursor and parsed is None:
        return error_json(400, "invalid_cursor", "Cursor is invalid.")
    items = repo.list_events(
        project_id,
        limit=limit,
        offset=offset,
        event_type=event_type,
        cursor=parsed,
    )
    if items and len(items) == limit:
        last = items[-1]
        response.headers["X-Next-Cursor"] = encode_cursor(last.created_at, last.id)
    return items
