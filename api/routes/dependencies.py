from fastapi import Request

from api.models.common import error_json
from api.services.platform.repository import PlatformRepository


def get_repo(request: Request) -> PlatformRepository:
    return request.app.state.platform_repo


def get_actor(request: Request) -> tuple[str, str | None]:
    tenant_claims = getattr(request.state, "tenant_claims", None)
    if tenant_claims is not None:
        return "client", tenant_claims.sub
    return "internal", None


def require_write_access(request: Request):
    tenant_claims = getattr(request.state, "tenant_claims", None)
    if tenant_claims is None:
        return None
    # Internal calls (no tenant claims) are trusted; tenant calls are role-gated.
    allowed = {"client_owner", "client_admin", "developer"}
    if tenant_claims.role in allowed:
        return None
    return error_json(403, "tenant_forbidden", "Tenant role is not allowed to perform write operations.")
