def test_full_demo_journey_intake_to_deploy(client, auth_headers):
    demo = client.post(
        "/v1/demo/bootstrap",
        headers=auth_headers,
        json={
            "org_name": "Journey Org",
            "org_slug": "journey-org",
            "project_name": "Journey Project",
            "app_name": "Journey App",
            "app_slug": "journey-app",
        },
    )
    assert demo.status_code == 200
    demo_body = demo.json()
    org_id = demo_body["organization"]["id"]
    project_id = demo_body["project"]["id"]

    intake = client.post(
        "/v1/intake-requests",
        headers=auth_headers,
        json={
            "organization_id": org_id,
            "project_id": project_id,
            "request_type": "enhancement",
            "title": "Demo journey request",
            "goal": "Validate full intake to deploy lifecycle",
        },
    )
    assert intake.status_code == 200
    intake_body = intake.json()
    intake_id = intake_body["id"]
    assert intake_body["status"] == "submitted"

    triaged = client.post(
        f"/v1/intake-requests/{intake_id}/triage",
        headers=auth_headers,
        json={"owner_user_id": "founder_demo", "priority": "high"},
    )
    assert triaged.status_code == 200
    assert triaged.json()["priority"] == "high"

    building = client.post(
        f"/v1/intake-requests/{intake_id}/status",
        headers=auth_headers,
        json={"status": "building"},
    )
    assert building.status_code == 200
    assert building.json()["status"] == "building"

    preview_created = client.post(
        "/v1/preview-builds",
        headers=auth_headers,
        json={
            "intake_request_id": intake_id,
            "build_version": "v1.0.0-preview.1",
            "preview_url": "https://preview.example.com/journey-v1",
            "notes": "Demo preview build",
        },
    )
    assert preview_created.status_code == 200
    preview = preview_created.json()

    preview_ready = client.post(
        f"/v1/preview-builds/{preview['id']}/status",
        headers=auth_headers,
        json={"status": "ready"},
    )
    assert preview_ready.status_code == 200
    assert preview_ready.json()["status"] == "ready"

    approved = client.post(
        "/v1/approval-decisions",
        headers=auth_headers,
        json={
            "intake_request_id": intake_id,
            "preview_build_id": preview["id"],
            "decision": "approve",
            "comments": "Approved for production release.",
        },
    )
    assert approved.status_code == 200
    assert approved.json()["decision"] == "approve"

    release_created = client.post(
        "/v1/releases",
        headers=auth_headers,
        json={
            "intake_request_id": intake_id,
            "preview_build_id": preview["id"],
            "notes": "Promote approved preview to production",
        },
    )
    assert release_created.status_code == 200
    release = release_created.json()
    assert release["status"] == "pending"

    release_deployed = client.post(
        f"/v1/releases/{release['id']}/status",
        headers=auth_headers,
        json={
            "status": "deployed",
            "release_url": "https://prod.example.com/journey-app",
            "notes": "Production rollout complete",
        },
    )
    assert release_deployed.status_code == 200
    assert release_deployed.json()["status"] == "deployed"

    intake_list = client.get(f"/v1/intake-requests?organization_id={org_id}", headers=auth_headers)
    assert intake_list.status_code == 200
    all_requests = intake_list.json()
    matching = [item for item in all_requests if item["id"] == intake_id]
    assert len(matching) == 1
    assert matching[0]["status"] == "deployed"
