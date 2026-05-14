def test_create_list_and_update_client_environment(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Env", "slug": "org-env"}).json()
    project = client.post(
        "/v1/projects",
        headers=auth_headers,
        json={"organization_id": org["id"], "name": "Env Project"},
    ).json()
    app = client.post(
        "/v1/apps",
        headers=auth_headers,
        json={
            "project_id": project["id"],
            "name": "Env App",
            "slug": "env-app",
            "deploy_mode": "platform_subdomain",
            "platform_subdomain": "env-app-sub",
        },
    ).json()

    created = client.post(
        "/v1/client-environments",
        headers=auth_headers,
        json={
            "app_id": app["id"],
            "name": "Production",
            "environment_type": "production",
            "base_url": "https://prod.example.com/env-app",
            "region": "us-west",
            "notes": "Primary production env",
        },
    )
    assert created.status_code == 200
    env = created.json()
    assert env["status"] == "provisioning"
    assert env["environment_type"] == "production"

    listed = client.get(f"/v1/client-environments?app_id={app['id']}", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.post(
        f"/v1/client-environments/{env['id']}",
        headers=auth_headers,
        json={
            "status": "active",
            "region": "us-east",
            "notes": "Promoted and healthy",
        },
    )
    assert updated.status_code == 200
    body = updated.json()
    assert body["status"] == "active"
    assert body["region"] == "us-east"


def test_client_environment_create_is_idempotent(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Env Idem", "slug": "org-env-idem"}).json()
    project = client.post(
        "/v1/projects",
        headers=auth_headers,
        json={"organization_id": org["id"], "name": "Env Idem Project"},
    ).json()
    app = client.post(
        "/v1/apps",
        headers=auth_headers,
        json={
            "project_id": project["id"],
            "name": "Env Idem App",
            "slug": "env-idem-app",
            "deploy_mode": "platform_subdomain",
            "platform_subdomain": "env-idem-sub",
        },
    ).json()

    headers = dict(auth_headers)
    headers["Idempotency-Key"] = "client-env-create-1"
    payload = {
        "app_id": app["id"],
        "name": "Preview",
        "environment_type": "preview",
        "base_url": "https://preview.example.com/env-idem",
    }
    first = client.post("/v1/client-environments", headers=headers, json=payload)
    second = client.post("/v1/client-environments", headers=headers, json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
