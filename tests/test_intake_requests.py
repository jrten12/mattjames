def test_create_list_and_update_intake_request(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Intake", "slug": "org-intake"}).json()
    project = client.post(
        "/v1/projects",
        headers=auth_headers,
        json={"organization_id": org["id"], "name": "Portal Refresh"},
    ).json()

    created = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org["id"],
            "project_id": project["id"],
            "request_type": "update",
            "title": "Add intake stepper",
            "goal": "Help clients submit cleaner briefs.",
            "details": "Need a simple wizard and attachments placeholder.",
        },
    )
    assert created.status_code == 200
    intake_request = created.json()
    assert intake_request["status"] == "submitted"

    listed = client.get(f"/v1/intake-requests?organization_id={org['id']}", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.post(
        f"/v1/intake-requests/{intake_request['id']}/status",
        headers=auth_headers,
        json={"status": "triaged"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "triaged"
    assert updated.json()["priority"] == "normal"
    assert updated.json()["owner_user_id"] is None

    triaged = client.post(
        f"/v1/intake-requests/{intake_request['id']}/triage",
        headers=auth_headers,
        json={"owner_user_id": "matt", "priority": "high"},
    )
    assert triaged.status_code == 200
    assert triaged.json()["owner_user_id"] == "matt"
    assert triaged.json()["priority"] == "high"


def test_intake_request_idempotency_for_create(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Idem Intake", "slug": "org-idem-intake"}).json()
    headers = dict(auth_headers)
    headers["Idempotency-Key"] = "intake-create-1"
    payload = {
        "organization_id": org["id"],
        "request_type": "new_app",
        "title": "Create patient triage assistant",
        "goal": "Reduce nurse triage time",
    }

    first = client.post("/v1/intake-requests", headers=headers, json=payload)
    second = client.post("/v1/intake-requests", headers=headers, json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]


def test_intake_request_rejects_project_from_different_org(client, auth_headers):
    org_a = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org A Intake", "slug": "org-a-intake"}).json()
    org_b = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org B Intake", "slug": "org-b-intake"}).json()
    project_b = client.post(
        "/v1/projects",
        headers=auth_headers,
        json={"organization_id": org_b["id"], "name": "B Project"},
    ).json()

    response = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org_a["id"],
            "project_id": project_b["id"],
            "request_type": "enhancement",
            "title": "Cross-org mismatch",
            "goal": "Should fail",
        },
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "project_scope_conflict"
