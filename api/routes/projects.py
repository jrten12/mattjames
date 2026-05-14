from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response

from api.models.common import ErrorResponse, error_json
from api.models.platform import Project, ProjectCreate, ProjectState
from api.pagination import decode_cursor, encode_cursor
from api.routes.dependencies import get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.routes.scope import enforce_org_scope
from api.services.platform.repository import NotFoundError, PlatformRepository

router = APIRouter()


@router.post("/projects", response_model=Project, responses={404: {"model": ErrorResponse}})
def create_project(
    body: ProjectCreate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    scope_err = enforce_org_scope(request, body.organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"create_project:{body.organization_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    try:
        created = repo.create_project(body)
        store_idempotent_result(
            repo,
            operation=f"create_project:{body.organization_id}",
            key=idempotency_key,
            payload=payload,
            status_code=200,
            response_json=created.model_dump(mode="json"),
        )
        return created
    except NotFoundError:
        return error_json(404, "organization_not_found", "Organization does not exist.")


@router.get("/projects", response_model=list[Project], responses={403: {"model": ErrorResponse}})
def list_projects(
    request: Request,
    response: Response,
    organization_id: UUID = Query(...),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    state: ProjectState | None = Query(default=None),
    cursor: str | None = Query(default=None),
    repo: PlatformRepository = Depends(get_repo),
):
    scope_err = enforce_org_scope(request, organization_id)
    if scope_err is not None:
        return scope_err
    parsed = decode_cursor(cursor) if cursor else None
    if cursor and parsed is None:
        return error_json(400, "invalid_cursor", "Cursor is invalid.")
    items = repo.list_projects(
        organization_id,
        limit=limit,
        offset=offset,
        state=state,
        cursor=parsed,
    )
    if items and len(items) == limit:
        last = items[-1]
        response.headers["X-Next-Cursor"] = encode_cursor(last.created_at, last.id)
    return items
