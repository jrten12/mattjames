from uuid import UUID

from fastapi import Request

from api.models.common import error_json


def enforce_org_scope(request: Request, organization_id: UUID):
    tenant_id = getattr(request.state, "tenant_id", None)
    if tenant_id is None:
        return None
    if tenant_id != str(organization_id):
        return error_json(403, "tenant_scope_mismatch", "Tenant scope does not match resource.")
    return None
