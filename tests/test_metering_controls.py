import os

import jwt
from fastapi.testclient import TestClient

from api.config import reset_settings_cache
from api.main import app


def test_admin_metering_policy_upsert_and_get(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Meter", "slug": "org-meter"}).json()

    upsert = client.post(
        f"/v1/admin/metering/{org['id']}",
        headers=auth_headers,
        json={
            "base_fee_cents": 25000,
            "usage_cap": 100000,
            "overage_behavior": "throttle",
            "is_enforced": True,
            "notes": "Phase rollout policy",
        },
    )
    assert upsert.status_code == 200
    body = upsert.json()
    assert body["base_fee_cents"] == 25000
    assert body["overage_behavior"] == "throttle"

    fetched = client.get(f"/v1/admin/metering/{org['id']}", headers=auth_headers)
    assert fetched.status_code == 200
    assert fetched.json()["usage_cap"] == 100000


def test_admin_metering_policy_idempotency(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Meter Idem", "slug": "org-meter-idem"}).json()
    headers = dict(auth_headers)
    headers["Idempotency-Key"] = "metering-upsert-1"
    payload = {
        "base_fee_cents": 1000,
        "usage_cap": 9999,
        "overage_behavior": "allow",
        "is_enforced": False,
    }
    first = client.post(f"/v1/admin/metering/{org['id']}", headers=headers, json=payload)
    second = client.post(f"/v1/admin/metering/{org['id']}", headers=headers, json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()


def test_tenant_cannot_use_founder_metering_controls():
    os.environ["PLATFORM_API_KEYS"] = "test-api-key"
    os.environ["USE_INMEMORY_STORE"] = "true"
    os.environ["ENFORCE_TENANT_JWT"] = "true"
    os.environ["TENANT_JWT_SECRET"] = "a-very-long-tenant-secret-for-tests"
    os.environ["TENANT_JWT_ISSUER"] = "mattjames-auth"
    os.environ["TENANT_JWT_AUDIENCE"] = "mattjames-platform"
    reset_settings_cache()

    token = jwt.encode(
        {
            "sub": "usr_meter_client",
            "tenant_id": "ten_meter",
            "role": "client_admin",
            "iss": "mattjames-auth",
            "aud": "mattjames-platform",
        },
        "a-very-long-tenant-secret-for-tests",
        algorithm="HS256",
    )
    headers = {"Authorization": f"Bearer {token}", "X-API-Key": "test-api-key"}

    with TestClient(app) as tc:
        org = tc.post("/v1/orgs", headers=headers, json={"name": "Meter Org", "slug": "meter-org"}).json()
        blocked = tc.post(
            f"/v1/admin/metering/{org['id']}",
            headers=headers,
            json={
                "base_fee_cents": 5000,
                "usage_cap": 12345,
                "overage_behavior": "pause",
                "is_enforced": True,
            },
        )
        assert blocked.status_code == 403
        assert blocked.json()["error"]["code"] == "founder_only"

    os.environ["ENFORCE_TENANT_JWT"] = "false"
    reset_settings_cache()
