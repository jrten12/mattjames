import os

import jwt
from fastapi.testclient import TestClient

from api.config import reset_settings_cache
from api.main import app


def test_viewer_role_cannot_write():
    os.environ["PLATFORM_API_KEYS"] = "test-api-key"
    os.environ["USE_INMEMORY_STORE"] = "true"
    os.environ["ENFORCE_TENANT_JWT"] = "true"
    os.environ["TENANT_JWT_SECRET"] = "a-very-long-tenant-secret-for-tests"
    os.environ["TENANT_JWT_ISSUER"] = "mattjames-auth"
    os.environ["TENANT_JWT_AUDIENCE"] = "mattjames-platform"
    reset_settings_cache()

    token = jwt.encode(
        {
            "sub": "usr_2",
            "tenant_id": "ten_viewer",
            "role": "viewer",
            "iss": "mattjames-auth",
            "aud": "mattjames-platform",
        },
        "a-very-long-tenant-secret-for-tests",
        algorithm="HS256",
    )
    headers = {"Authorization": f"Bearer {token}", "X-API-Key": "test-api-key"}

    with TestClient(app) as client:
        blocked = client.post("/v1/orgs", headers=headers, json={"name": "Viewer Org", "slug": "viewer-org"})
        assert blocked.status_code == 403
        assert blocked.json()["error"]["code"] == "tenant_forbidden"

    os.environ["ENFORCE_TENANT_JWT"] = "false"
    reset_settings_cache()
