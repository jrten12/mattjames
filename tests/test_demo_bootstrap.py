def test_demo_bootstrap_creates_org_project_app(client, auth_headers):
    response = client.post(
        "/v1/demo/bootstrap",
        headers=auth_headers,
        json={
            "org_name": "Demo Clinic",
            "org_slug": "demo-clinic",
            "owner_user_id": "owner_demo",
            "project_name": "Demo Project",
            "app_name": "Demo App",
            "app_slug": "demo-app",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["organization"]["slug"] == "demo-clinic"
    assert body["project"]["organization_id"] == body["organization"]["id"]
    assert body["app"]["project_id"] == body["project"]["id"]
    assert body["owner_member"]["organization_id"] == body["organization"]["id"]


def test_demo_bootstrap_conflict_on_existing_slug(client, auth_headers):
    first = client.post(
        "/v1/demo/bootstrap",
        headers=auth_headers,
        json={"org_slug": "demo-repeat"},
    )
    assert first.status_code == 200

    second = client.post(
        "/v1/demo/bootstrap",
        headers=auth_headers,
        json={"org_slug": "demo-repeat"},
    )
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "demo_conflict"
