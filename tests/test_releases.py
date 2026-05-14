def test_create_list_and_update_release_record(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Release", "slug": "org-release"}).json()
    intake = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "request_type": "new_app",
            "title": "Release app",
            "goal": "Ship release flow",
        },
    ).json()
    preview = client.post(
        "/v1/preview-builds",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "build_version": "v0.2.0-preview.1",
            "preview_url": "https://preview.example.com/r1",
        },
    ).json()
    client.post(
        f"/v1/preview-builds/{preview['id']}/status",
        headers=auth_headers,
        json={"status": "ready"},
    )
    client.post(
        "/v1/approval-decisions",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "preview_build_id": preview["id"],
            "decision": "approve",
            "comments": "Approved for release.",
        },
    )

    created = client.post(
        "/v1/releases",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "preview_build_id": preview["id"],
            "notes": "Promote to production",
        },
    )
    assert created.status_code == 200
    release = created.json()
    assert release["status"] == "pending"
    assert release["build_version"] == "v0.2.0-preview.1"

    listed = client.get(f"/v1/releases?intake_request_id={intake['id']}", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.post(
        f"/v1/releases/{release['id']}/status",
        headers=auth_headers,
        json={"status": "deployed", "release_url": "https://prod.example.com/r1"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "deployed"
    assert updated.json()["release_url"] == "https://prod.example.com/r1"

    intake_list = client.get(f"/v1/intake-requests?organization_id={org['id']}", headers=auth_headers).json()
    assert intake_list[0]["status"] == "deployed"


def test_release_creation_requires_ready_preview_and_approval(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Release B", "slug": "org-release-b"}).json()
    intake = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "request_type": "update",
            "title": "Release gate",
            "goal": "Verify release constraints",
        },
    ).json()
    preview = client.post(
        "/v1/preview-builds",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "build_version": "v1",
            "preview_url": "https://preview.example.com/r2",
        },
    ).json()

    no_ready = client.post(
        "/v1/releases",
        headers=auth_headers,
        json={"intake_request_id": intake["id"], "preview_build_id": preview["id"]},
    )
    assert no_ready.status_code == 409
    assert no_ready.json()["error"]["code"] == "preview_not_ready"

    client.post(
        f"/v1/preview-builds/{preview['id']}/status",
        headers=auth_headers,
        json={"status": "ready"},
    )
    no_approval = client.post(
        "/v1/releases",
        headers=auth_headers,
        json={"intake_request_id": intake["id"], "preview_build_id": preview["id"]},
    )
    assert no_approval.status_code == 409
    assert no_approval.json()["error"]["code"] == "release_not_approved"


def test_release_create_is_idempotent(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Release Idem", "slug": "org-release-idem"}).json()
    intake = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "request_type": "enhancement",
            "title": "Release idem",
            "goal": "Verify release idempotency",
        },
    ).json()
    preview = client.post(
        "/v1/preview-builds",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "build_version": "v1",
            "preview_url": "https://preview.example.com/idem",
        },
    ).json()
    client.post(
        f"/v1/preview-builds/{preview['id']}/status",
        headers=auth_headers,
        json={"status": "ready"},
    )
    client.post(
        "/v1/approval-decisions",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "preview_build_id": preview["id"],
            "decision": "approve",
        },
    )

    headers = dict(auth_headers)
    headers["Idempotency-Key"] = "release-create-1"
    payload = {"intake_request_id": intake["id"], "preview_build_id": preview["id"]}
    first = client.post("/v1/releases", headers=headers, json=payload)
    second = client.post("/v1/releases", headers=headers, json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]
