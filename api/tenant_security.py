from dataclasses import dataclass
from typing import Any

import jwt
from fastapi import Request
from jwt import InvalidTokenError

from api.config import Settings
from api.models.common import error_json


@dataclass
class TenantClaims:
    tenant_id: str
    app_id: str | None
    sub: str
    role: str | None


def _extract_bearer_token(request: Request) -> str | None:
    header = request.headers.get("authorization")
    if not header or not header.lower().startswith("bearer "):
        return None
    return header[7:].strip() or None


def _parse_claims(payload: dict[str, Any]) -> TenantClaims | None:
    tenant_id = payload.get("tenant_id")
    sub = payload.get("sub")
    if not isinstance(tenant_id, str) or not isinstance(sub, str):
        return None
    app_id = payload.get("app_id")
    role = payload.get("role")
    return TenantClaims(
        tenant_id=tenant_id,
        app_id=app_id if isinstance(app_id, str) else None,
        sub=sub,
        role=role if isinstance(role, str) else None,
    )


def validate_tenant_token_for_request(request: Request, settings: Settings):
    if not settings.enforce_tenant_jwt:
        return None, None
    if not settings.tenant_jwt_secret.strip():
        return None, error_json(503, "tenant_auth_not_configured", "Tenant JWT auth is not configured.")

    token = _extract_bearer_token(request)
    if token is None:
        return None, error_json(401, "missing_tenant_token", "Missing tenant token.")

    try:
        payload = jwt.decode(
            token,
            settings.tenant_jwt_secret,
            algorithms=["HS256"],
            issuer=settings.tenant_jwt_issuer,
            audience=settings.tenant_jwt_audience,
        )
    except InvalidTokenError:
        return None, error_json(403, "invalid_tenant_token", "Invalid tenant token.")

    claims = _parse_claims(payload)
    if claims is None:
        return None, error_json(403, "invalid_tenant_token", "Invalid tenant token.")

    x_tenant = request.headers.get("x-tenant-id")
    if x_tenant and x_tenant != claims.tenant_id:
        return None, error_json(403, "tenant_scope_mismatch", "Tenant scope does not match token.")
    x_app = request.headers.get("x-app-id")
    if x_app and claims.app_id and x_app != claims.app_id:
        return None, error_json(403, "tenant_scope_mismatch", "App scope does not match token.")
    return claims, None
