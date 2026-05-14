import hashlib
import json
from typing import Any

from fastapi.responses import JSONResponse

from api.models.platform import IdempotencyRecord
from api.services.platform.repository import PlatformRepository


def _request_fingerprint(payload: dict[str, Any]) -> str:
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def restore_if_idempotent(
    repo: PlatformRepository,
    *,
    operation: str,
    key: str | None,
    payload: dict[str, Any],
):
    if not key:
        return None
    existing = repo.get_idempotency_record(operation, key)
    if existing is None:
        return None
    if existing.request_fingerprint != _request_fingerprint(payload):
        return JSONResponse(
            status_code=409,
            content={
                "error": {
                    "code": "idempotency_key_reused",
                    "message": "Idempotency key was reused with a different payload.",
                    "request_id": "req_idempotency_conflict",
                }
            },
        )
    return JSONResponse(status_code=existing.status_code, content=existing.response_json)


def store_idempotent_result(
    repo: PlatformRepository,
    *,
    operation: str,
    key: str | None,
    payload: dict[str, Any],
    status_code: int,
    response_json: dict[str, Any],
) -> None:
    if not key:
        return
    repo.save_idempotency_record(
        IdempotencyRecord(
            key=key,
            operation=operation,
            request_fingerprint=_request_fingerprint(payload),
            status_code=status_code,
            response_json=response_json,
        )
    )
