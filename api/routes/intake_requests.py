from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response

from api.models.common import ErrorResponse, error_json
from api.models.platform import (
    IntakeRequest,
    IntakeRequestCreate,
    IntakeRequestStatus,
    IntakeRequestStatusUpdate,
    IntakeRequestTriageUpdate,
)
from api.pagination import decode_cursor, encode_cursor
from api.routes.dependencies import get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.routes.scope import enforce_org_scope
from api.services.platform.repository import ConflictError, NotFoundError, PlatformRepository

router = APIRouter()


@router.post(
    "/intake-requests",
    response_model=IntakeRequest,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def create_intake_request(
    body: IntakeRequestCreate,
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
        operation=f"create_intake_request:{body.organization_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    try:
        created = repo.create_intake_request(body)
        store_idempotent_result(
            repo,
            operation=f"create_intake_request:{body.organization_id}",
            key=idempotency_key,
            payload=payload,
            status_code=200,
            response_json=created.model_dump(mode="json"),
        )
        return created
    except NotFoundError:
        return error_json(404, "organization_not_found", "Organization does not exist.")
    except ConflictError:
        return error_json(409, "project_scope_conflict", "Project does not belong to organization.")


@router.get(
    "/intake-requests",
    response_model=list[IntakeRequest],
    responses={403: {"model": ErrorResponse}},
)
def list_intake_requests(
    request: Request,
    response: Response,
    organization_id: UUID = Query(...),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    status: IntakeRequestStatus | None = Query(default=None),
    request_type: str | None = Query(default=None),
    cursor: str | None = Query(default=None),
    repo: PlatformRepository = Depends(get_repo),
):
    scope_err = enforce_org_scope(request, organization_id)
    if scope_err is not None:
        return scope_err
    parsed = decode_cursor(cursor) if cursor else None
    if cursor and parsed is None:
        return error_json(400, "invalid_cursor", "Cursor is invalid.")
    items = repo.list_intake_requests(
        organization_id,
        limit=limit,
        offset=offset,
        status=status,
        request_type=request_type,
        cursor=parsed,
    )
    if items and len(items) == limit:
        last = items[-1]
        response.headers["X-Next-Cursor"] = encode_cursor(last.created_at, last.id)
    return items


@router.post(
    "/intake-requests/{intake_request_id}/status",
    response_model=IntakeRequest,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def update_intake_request_status(
    intake_request_id: UUID,
    body: IntakeRequestStatusUpdate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    try:
        current = repo.get_intake_request(intake_request_id)
    except NotFoundError:
        return error_json(404, "intake_request_not_found", "Intake request does not exist.")
    scope_err = enforce_org_scope(request, current.organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"update_intake_request_status:{intake_request_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    updated = repo.update_intake_request_status(intake_request_id, body.status)
    store_idempotent_result(
        repo,
        operation=f"update_intake_request_status:{intake_request_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=updated.model_dump(mode="json"),
    )
    return updated


@router.post(
    "/intake-requests/{intake_request_id}/triage",
    response_model=IntakeRequest,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def update_intake_request_triage(
    intake_request_id: UUID,
    body: IntakeRequestTriageUpdate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    write_err = require_write_access(request)
    if write_err is not None:
        return write_err
    try:
        current = repo.get_intake_request(intake_request_id)
    except NotFoundError:
        return error_json(404, "intake_request_not_found", "Intake request does not exist.")
    scope_err = enforce_org_scope(request, current.organization_id)
    if scope_err is not None:
        return scope_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"update_intake_request_triage:{intake_request_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    updated = repo.update_intake_request_triage(intake_request_id, body)
    store_idempotent_result(
        repo,
        operation=f"update_intake_request_triage:{intake_request_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=updated.model_dump(mode="json"),
    )
    return updated
