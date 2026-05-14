from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response

from api.models.common import ErrorResponse, error_json
from api.models.platform import (
    ClientEnvironmentCreate,
    ClientEnvironmentRecord,
    ClientEnvironmentStatus,
    ClientEnvironmentUpdate,
)
from api.pagination import decode_cursor, encode_cursor
from api.routes.dependencies import get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.routes.scope import enforce_org_scope
from api.services.platform.repository import NotFoundError, PlatformRepository

router = APIRouter()


@router.post(
    "/client-environments",
    response_model=ClientEnvironmentRecord,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def create_client_environment(
    body: ClientEnvironmentCreate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    try:
        app = repo.get_app(body.app_id)
        project = repo.get_project(app.project_id)
    except NotFoundError:
        return error_json(404, "app_not_found", "App does not exist.")
    scope_err = enforce_org_scope(request, project.organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"create_client_environment:{body.app_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    created = repo.create_client_environment(body)
    store_idempotent_result(
        repo,
        operation=f"create_client_environment:{body.app_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=created.model_dump(mode="json"),
    )
    return created


@router.get(
    "/client-environments",
    response_model=list[ClientEnvironmentRecord],
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def list_client_environments(
    request: Request,
    response: Response,
    app_id: UUID = Query(...),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: ClientEnvironmentStatus | None = Query(default=None),
    cursor: str | None = Query(default=None),
    repo: PlatformRepository = Depends(get_repo),
):
    try:
        app = repo.get_app(app_id)
        project = repo.get_project(app.project_id)
    except NotFoundError:
        return error_json(404, "app_not_found", "App does not exist.")
    scope_err = enforce_org_scope(request, project.organization_id)
    if scope_err is not None:
        return scope_err
    parsed = decode_cursor(cursor) if cursor else None
    if cursor and parsed is None:
        return error_json(400, "invalid_cursor", "Cursor is invalid.")
    items = repo.list_client_environments(
        app_id,
        limit=limit,
        offset=offset,
        status=status,
        cursor=parsed,
    )
    if items and len(items) == limit:
        last = items[-1]
        response.headers["X-Next-Cursor"] = encode_cursor(last.created_at, last.id)
    return items


@router.post(
    "/client-environments/{environment_id}",
    response_model=ClientEnvironmentRecord,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def update_client_environment(
    environment_id: UUID,
    body: ClientEnvironmentUpdate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    try:
        current = repo.get_client_environment(environment_id)
    except NotFoundError:
        return error_json(404, "client_environment_not_found", "Client environment does not exist.")
    scope_err = enforce_org_scope(request, current.organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"update_client_environment:{environment_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    updated = repo.update_client_environment(environment_id, body)
    store_idempotent_result(
        repo,
        operation=f"update_client_environment:{environment_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=updated.model_dump(mode="json"),
    )
    return updated
