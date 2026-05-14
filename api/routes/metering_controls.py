from uuid import UUID

from fastapi import APIRouter, Depends, Header, Request

from api.models.common import ErrorResponse, error_json
from api.models.platform import MeteringPolicyRecord, MeteringPolicyUpsert
from api.routes.dependencies import get_repo, require_internal_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.services.platform.repository import NotFoundError, PlatformRepository

router = APIRouter()


@router.get(
    "/admin/metering/{organization_id}",
    response_model=MeteringPolicyRecord,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def get_metering_policy(
    organization_id: UUID,
    request: Request,
    repo: PlatformRepository = Depends(get_repo),
):
    internal_err = require_internal_access(request)
    if internal_err is not None:
        return internal_err
    try:
        return repo.get_metering_policy(organization_id)
    except NotFoundError as exc:
        msg = str(exc)
        if "Organization" in msg:
            return error_json(404, "organization_not_found", "Organization does not exist.")
        return error_json(404, "metering_policy_not_found", "Metering policy is not configured.")


@router.post(
    "/admin/metering/{organization_id}",
    response_model=MeteringPolicyRecord,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def upsert_metering_policy(
    organization_id: UUID,
    body: MeteringPolicyUpsert,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repo: PlatformRepository = Depends(get_repo),
):
    internal_err = require_internal_access(request)
    if internal_err is not None:
        return internal_err
    payload = body.model_dump(mode="json")
    restored = restore_if_idempotent(
        repo,
        operation=f"upsert_metering_policy:{organization_id}",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored
    try:
        updated = repo.upsert_metering_policy(organization_id, body)
    except NotFoundError:
        return error_json(404, "organization_not_found", "Organization does not exist.")
    store_idempotent_result(
        repo,
        operation=f"upsert_metering_policy:{organization_id}",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=updated.model_dump(mode="json"),
    )
    return updated
