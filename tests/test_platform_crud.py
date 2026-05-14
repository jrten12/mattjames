def test_create_and_list_orgs(client, auth_headers):
    created = client.post(
        "/v1/orgs",
        headers=auth_headers,
        json={"name": "Acme Health", "slug": "acme-health", "billing_email": "ops@acme.com"},
    )
    assert created.status_code == 200
    body = created.json()
    assert body["slug"] == "acme-health"

    listed = client.get("/v1/orgs", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_create_project_and_apps(client, auth_headers):
    org = client.post(
        "/v1/orgs",
        headers=auth_headers,
        json={"name": "Beta", "slug": "beta-org"},
    ).json()

    project = client.post(
        "/v1/projects",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "name": "Claims Bot",
            "description": "Phase 1 app",
        },
    )
    assert project.status_code == 200
    project_json = project.json()
    assert project_json["current_state"] == "intake"

    created_app = client.post(
        "/v1/apps",
        headers=auth_headers,
        json={
            "project_id": project_json["id"],
            "name": "Claims Intake",
            "slug": "claims-intake",
            "deploy_mode": "platform_subdomain",
            "platform_subdomain": "claims-beta",
        },
    )
    assert created_app.status_code == 200
    assert created_app.json()["slug"] == "claims-intake"

    listed = client.get(f"/v1/apps?project_id={project_json['id']}", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1
