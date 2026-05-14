from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response

from api.models.common import ErrorResponse, error_json
from api.models.platform import PreviewBuild, PreviewBuildCreate, PreviewBuildStatus, PreviewBuildStatusUpdate
from api.pagination import decode_cursor, encode_cursor
from api.routes.dependencies import get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.routes.scope import enforce_org_scope
from api.services.platform.repository import NotFoundError, PlatformRepository

router = APIRouter()


@router.post(
    "/preview-builds",
    response_model=PreviewBuild,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def create_preview_build(
    body: PreviewBuildCreate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    try:
        intake_request = repo.get_intake_request(body.intake_request_id)
    except NotFoundError:
        return error_json(404, "intake_request_not_found", "Intake request does not exist.")
    scope_err = enforce_org_scope(request, intake_request.organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"create_preview_build:{body.intake_request_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    created = repo.create_preview_build(body)
    store_idempotent_result(
        repo,
        operation=f"create_preview_build:{body.intake_request_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=created.model_dump(mode="json"),
    )
    return created


@router.get(
    "/preview-builds",
    response_model=list[PreviewBuild],
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def list_preview_builds(
    request: Request,
    response: Response,
    intake_request_id: UUID = Query(...),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: PreviewBuildStatus | None = Query(default=None),
    cursor: str | None = Query(default=None),
    repo: PlatformRepository = Depends(get_repo),
):
    try:
        intake_request = repo.get_intake_request(intake_request_id)
    except NotFoundError:
        return error_json(404, "intake_request_not_found", "Intake request does not exist.")
    scope_err = enforce_org_scope(request, intake_request.organization_id)
    if scope_err is not None:
        return scope_err
    parsed = decode_cursor(cursor) if cursor else None
    if cursor and parsed is None:
        return error_json(400, "invalid_cursor", "Cursor is invalid.")
    items = repo.list_preview_builds(
        intake_request_id,
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
    "/preview-builds/{preview_build_id}/status",
    response_model=PreviewBuild,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def update_preview_build_status(
    preview_build_id: UUID,
    body: PreviewBuildStatusUpdate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    try:
        current = repo.get_preview_build(preview_build_id)
    except NotFoundError:
        return error_json(404, "preview_build_not_found", "Preview build does not exist.")
    scope_err = enforce_org_scope(request, current.organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"update_preview_build_status:{preview_build_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    updated = repo.update_preview_build_status(preview_build_id, body)
    store_idempotent_result(
        repo,
        operation=f"update_preview_build_status:{preview_build_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=updated.model_dump(mode="json"),
    )
    return updated
