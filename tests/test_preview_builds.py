def test_create_list_and_update_preview_build(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Preview", "slug": "org-preview"}).json()
    intake = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "request_type": "new_app",
            "title": "Preview app",
            "goal": "Ship preview flow",
        },
    ).json()

    created = client.post(
        "/v1/preview-builds",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "build_version": "v0.1.0-preview.1",
            "preview_url": "https://preview.example.com/build-1",
            "notes": "Initial preview build",
        },
    )
    assert created.status_code == 200
    build = created.json()
    assert build["status"] == "queued"

    listed = client.get(f"/v1/preview-builds?intake_request_id={intake['id']}", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.post(
        f"/v1/preview-builds/{build['id']}/status",
        headers=auth_headers,
        json={"status": "ready"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "ready"


def test_preview_build_create_is_idempotent(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org PB Idem", "slug": "org-pb-idem"}).json()
    intake = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "request_type": "enhancement",
            "title": "PB idem",
            "goal": "Verify idempotency",
        },
    ).json()

    headers = dict(auth_headers)
    headers["Idempotency-Key"] = "preview-build-create-1"
    payload = {
        "intake_request_id": intake["id"],
        "build_version": "v1",
        "preview_url": "https://preview.example.com/v1",
    }
    first = client.post("/v1/preview-builds", headers=headers, json=payload)
    second = client.post("/v1/preview-builds", headers=headers, json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
