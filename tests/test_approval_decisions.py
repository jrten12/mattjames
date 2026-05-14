def test_create_approval_decision_updates_intake_status(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Approval", "slug": "org-approval"}).json()
    intake = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "request_type": "new_app",
            "title": "Approval request",
            "goal": "Test approval flow",
        },
    ).json()
    preview = client.post(
        "/v1/preview-builds",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "build_version": "v0.1.0-preview.1",
            "preview_url": "https://preview.example.com/a1",
        },
    ).json()

    created = client.post(
        "/v1/approval-decisions",
        headers=auth_headers,
        json={
            "intake_request_id": intake["id"],
            "preview_build_id": preview["id"],
            "decision": "request_changes",
            "comments": "Please update onboarding copy.",
        },
    )
    assert created.status_code == 200
    body = created.json()
    assert body["decision"] == "request_changes"
    assert body["intake_request_id"] == intake["id"]

    requests = client.get(f"/v1/intake-requests?organization_id={org['id']}", headers=auth_headers).json()
    assert requests[0]["status"] == "changes_requested"

    listed = client.get(f"/v1/approval-decisions?intake_request_id={intake['id']}", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_approval_decision_conflict_for_wrong_preview_build(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Approval B", "slug": "org-approval-b"}).json()
    intake_a = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "request_type": "update",
            "title": "Request A",
            "goal": "Goal A",
        },
    ).json()
    intake_b = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "request_type": "update",
            "title": "Request B",
            "goal": "Goal B",
        },
    ).json()
    preview_b = client.post(
        "/v1/preview-builds",
        headers=auth_headers,
        json={
            "intake_request_id": intake_b["id"],
            "build_version": "v1",
            "preview_url": "https://preview.example.com/b",
        },
    ).json()

    response = client.post(
        "/v1/approval-decisions",
        headers=auth_headers,
        json={
            "intake_request_id": intake_a["id"],
            "preview_build_id": preview_b["id"],
            "decision": "approve",
        },
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "approval_scope_conflict"
