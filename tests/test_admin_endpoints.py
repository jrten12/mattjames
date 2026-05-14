def _bootstrap(client, auth_headers):
    response = client.post(
        "/v1/demo/bootstrap",
        headers=auth_headers,
        json={
            "org_name": "Admin Demo",
            "org_slug": "admin-demo",
            "project_name": "Admin Project",
            "app_name": "Admin App",
            "app_slug": "admin-app",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_admin_pause_resume_project(client, auth_headers):
    demo = _bootstrap(client, auth_headers)
    project_id = demo["project"]["id"]

    paused = client.post(f"/v1/admin/projects/{project_id}/pause", headers=auth_headers, json={})
    assert paused.status_code == 200
    assert paused.json()["current_state"] == "paused"

    resumed = client.post(
        f"/v1/admin/projects/{project_id}/resume",
        headers=auth_headers,
        json={"to_state": "discovery_active"},
    )
    assert resumed.status_code == 200
    assert resumed.json()["current_state"] == "discovery_active"


def test_admin_update_app_status(client, auth_headers):
    demo = _bootstrap(client, auth_headers)
    app_id = demo["app"]["id"]
    updated = client.post(
        f"/v1/admin/apps/{app_id}/status",
        headers=auth_headers,
        json={"status": "active"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "active"


def test_admin_lookup_endpoints(client, auth_headers):
    demo = _bootstrap(client, auth_headers)
    org = client.get(f"/v1/admin/orgs/{demo['organization']['id']}", headers=auth_headers)
    project = client.get(f"/v1/admin/projects/{demo['project']['id']}", headers=auth_headers)
    app = client.get(f"/v1/admin/apps/{demo['app']['id']}", headers=auth_headers)

    assert org.status_code == 200
    assert project.status_code == 200
    assert app.status_code == 200
