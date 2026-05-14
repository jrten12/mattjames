from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, Request, Response

from api.models.common import ErrorResponse, error_json
from api.models.platform import ApprovalDecisionCreate, ApprovalDecisionRecord
from api.pagination import decode_cursor, encode_cursor
from api.routes.dependencies import get_repo
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.routes.scope import enforce_org_scope
from api.services.platform.repository import ConflictError, NotFoundError, PlatformRepository

router = APIRouter()


@router.post(
    "/approval-decisions",
    response_model=ApprovalDecisionRecord,
    responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def create_approval_decision(
    body: ApprovalDecisionCreate,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
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
        operation=f"create_approval_decision:{body.intake_request_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    decided_by = None
    tenant_claims = getattr(request.state, "tenant_claims", None)
    if tenant_claims is not None:
        decided_by = tenant_claims.sub
    try:
        created = repo.create_approval_decision(body, decided_by=decided_by)
    except NotFoundError:
        return error_json(404, "preview_build_not_found", "Preview build does not exist.")
    except ConflictError:
        return error_json(409, "approval_scope_conflict", "Preview build does not belong to intake request.")
    store_idempotent_result(
        repo,
        operation=f"create_approval_decision:{body.intake_request_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=created.model_dump(mode="json"),
    )
    return created


@router.get(
    "/approval-decisions",
    response_model=list[ApprovalDecisionRecord],
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def list_approval_decisions(
    request: Request,
    response: Response,
    intake_request_id: UUID = Query(...),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
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
    items = repo.list_approval_decisions(
        intake_request_id,
        limit=limit,
        offset=offset,
        cursor=parsed,
    )
    if items and len(items) == limit:
        last = items[-1]
        response.headers["X-Next-Cursor"] = encode_cursor(last.created_at, last.id)
    return items
