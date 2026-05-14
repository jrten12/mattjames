from fastapi import APIRouter, Depends, Header, Request

from api.models.common import ErrorResponse, error_json
from api.models.platform import (
    AppCreate,
    DemoBootstrapRequest,
    DemoBootstrapResponse,
    OrganizationCreate,
    OrganizationMemberCreate,
    ProjectCreate,
)
from api.routes.dependencies import get_repo, require_write_access
from api.routes.idempotency import restore_if_idempotent, store_idempotent_result
from api.services.platform.repository import ConflictError, PlatformRepository

router = APIRouter()


@router.post(
    "/demo/bootstrap",
    response_model=DemoBootstrapResponse,
    responses={409: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
)
def bootstrap_demo_org(
    body: DemoBootstrapRequest,
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
        operation="demo_bootstrap",
        key=idempotency_key,
        payload=payload,
    )
    if restored is not None:
        return restored

    try:
        organization = repo.create_organization(
            OrganizationCreate(
                name=body.org_name,
                slug=body.org_slug,
                billing_email=f"demo+{body.org_slug}@mattjames.local",
            )
        )
    except ConflictError:
        return error_json(
            409,
            "demo_conflict",
            "A demo organization with this slug already exists. Use a different org_slug.",
        )

    owner_member = repo.create_organization_member(
        organization.id,
        OrganizationMemberCreate(user_id=body.owner_user_id, role="client_owner"),
    )
    project = repo.create_project(
        ProjectCreate(
            organization_id=organization.id,
            name=body.project_name,
            description="Demo workspace for platform UI and workflow walkthroughs.",
        )
    )
    app = repo.create_app(
        AppCreate(
            project_id=project.id,
            name=body.app_name,
            slug=body.app_slug,
            deploy_mode="platform_subdomain",
            platform_subdomain=f"{body.app_slug}-{body.org_slug}",
        )
    )

    response = DemoBootstrapResponse(
        organization=organization,
        owner_member=owner_member,
        project=project,
        app=app,
    )
    store_idempotent_result(
        repo,
        operation="demo_bootstrap",
        key=idempotency_key,
        payload=payload,
        status_code=200,
        response_json=response.model_dump(mode="json"),
    )
    return response
