from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response

from api.models.common import ErrorResponse, error_json
from api.models.platform import App, AppCreate
from api.pagination import decode_cursor, encode_cursor
from api.routes.dependencies import get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.routes.scope import enforce_org_scope
from api.services.platform.repository import ConflictError, NotFoundError, PlatformRepository

router = APIRouter()


@router.post(
    "/apps",
    response_model=App,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def create_app(
    body: AppCreate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    try:
        project = repo.get_project(body.project_id)
    except NotFoundError:
        return error_json(404, "project_not_found", "Project does not exist.")
    scope_err = enforce_org_scope(request, project.organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"create_app:{project.id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    try:
        created = repo.create_app(body)
        store_idempotent_result(
            repo,
            operation=f"create_app:{project.id}",
            key=idempotency_key,
            payload=payload,
            status_code=200,
            response_json=created.model_dump(mode="json"),
        )
        return created
    except NotFoundError:
        return error_json(404, "project_not_found", "Project does not exist.")
    except ConflictError:
        return error_json(409, "app_conflict", "App slug already exists for this project.")


@router.get(
    "/apps",
    response_model=list[App],
    responses={403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def list_apps(
    request: Request,
    response: Response,
    project_id: UUID = Query(...),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: str | None = Query(default=None),
    deploy_mode: str | None = Query(default=None),
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
    items = repo.list_apps(
        project_id,
        limit=limit,
        offset=offset,
        status=status,
        deploy_mode=deploy_mode,
        cursor=parsed,
    )
    if items and len(items) == limit:
        last = items[-1]
        response.headers["X-Next-Cursor"] = encode_cursor(last.created_at, last.id)
    return items
