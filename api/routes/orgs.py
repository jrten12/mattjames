from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response

from api.models.common import ErrorResponse, error_json
from api.models.platform import Organization, OrganizationCreate, OrganizationMember, OrganizationMemberCreate
from api.pagination import decode_cursor, encode_cursor
from api.routes.dependencies import get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.routes.scope import enforce_org_scope
from api.services.platform.repository import ConflictError, NotFoundError, PlatformRepository

router = APIRouter()


@router.post("/orgs", response_model=Organization, responses={409: {"model": ErrorResponse}})
def create_org(
    body: OrganizationCreate,
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
        operation="create_org",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    try:
        created = repo.create_organization(body)
        store_idempotent_result(
            repo,
            operation="create_org",
            key=idempotency_key,
            payload=payload,
            status_code=200,
            response_json=created.model_dump(mode="json"),
        )
        return created
    except ConflictError:
        return error_json(409, "org_conflict", "Organization already exists.")


@router.get("/orgs", response_model=list[Organization])
def list_orgs(
    response: Response,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    slug: str | None = Query(default=None),
    cursor: str | None = Query(default=None),
    repo: PlatformRepository = Depends(get_repo),
):
    parsed = decode_cursor(cursor) if cursor else None
    if cursor and parsed is None:
        return error_json(400, "invalid_cursor", "Cursor is invalid.")
    items = repo.list_organizations(limit=limit, offset=offset, slug=slug, cursor=parsed)
    if items and len(items) == limit:
        last = items[-1]
        response.headers["X-Next-Cursor"] = encode_cursor(last.created_at, last.id)
    return items


@router.post(
    "/orgs/{organization_id}/members",
    response_model=OrganizationMember,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def create_org_member(
    organization_id: UUID,
    body: OrganizationMemberCreate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    scope_err = enforce_org_scope(request, organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"create_org_member:{organization_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    try:
        created = repo.create_organization_member(organization_id, body)
        store_idempotent_result(
            repo,
            operation=f"create_org_member:{organization_id}",
            key=idempotency_key,
            payload=payload,
            status_code=200,
            response_json=created.model_dump(mode="json"),
        )
        return created
    except NotFoundError:
        return error_json(404, "organization_not_found", "Organization does not exist.")
    except ConflictError:
        return error_json(409, "member_conflict", "Organization member already exists.")


@router.get(
    "/orgs/{organization_id}/members",
    response_model=list[OrganizationMember],
    responses={403: {"model": ErrorResponse}},
)
def list_org_members(
    organization_id: UUID,
    request: Request,
    response: Response,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    role: str | None = Query(default=None),
    cursor: str | None = Query(default=None),
    repo: PlatformRepository = Depends(get_repo),
):
    scope_err = enforce_org_scope(request, organization_id)
    if scope_err is not None:
        return scope_err
    parsed = decode_cursor(cursor) if cursor else None
    if cursor and parsed is None:
        return error_json(400, "invalid_cursor", "Cursor is invalid.")
    items = repo.list_organization_members(
        organization_id,
        limit=limit,
        offset=offset,
        role=role,
        cursor=parsed,
    )
    if items and len(items) == limit:
        last = items[-1]
        response.headers["X-Next-Cursor"] = encode_cursor(last.created_at, last.id)
    return items
