def test_org_list_pagination_and_slug_filter(client, auth_headers):
    client.post("/v1/orgs", headers=auth_headers, json={"name": "Org A", "slug": "org-a"})
    client.post("/v1/orgs", headers=auth_headers, json={"name": "Org B", "slug": "org-b"})

    filtered = client.get("/v1/orgs?slug=org-a", headers=auth_headers)
    assert filtered.status_code == 200
    assert len(filtered.json()) == 1
    assert filtered.json()[0]["slug"] == "org-a"

    paged = client.get("/v1/orgs?limit=1&offset=1", headers=auth_headers)
    assert paged.status_code == 200
    assert len(paged.json()) == 1

    first_page = client.get("/v1/orgs?limit=1", headers=auth_headers)
    assert first_page.status_code == 200
    assert len(first_page.json()) == 1
    next_cursor = first_page.headers.get("X-Next-Cursor")
    assert next_cursor
    second_page = client.get(f"/v1/orgs?limit=1&cursor={next_cursor}", headers=auth_headers)
    assert second_page.status_code == 200
    assert len(second_page.json()) == 1
    assert first_page.json()[0]["id"] != second_page.json()[0]["id"]


def test_projects_state_filter_and_apps_deploy_mode_filter(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org X", "slug": "org-x"}).json()
    project = client.post(
        "/v1/projects",
        headers=auth_headers,
        json={"organization_id": org["id"], "name": "Proj X"},
    ).json()

    client.post(
        f"/v1/projects/{project['id']}/transitions",
        headers=auth_headers,
        json={"to_state": "discovery_active", "reason_code": "kickoff"},
    )

    projects = client.get(
        f"/v1/projects?organization_id={org['id']}&state=discovery_active",
        headers=auth_headers,
    )
    assert projects.status_code == 200
    assert len(projects.json()) == 1

    client.post(
        "/v1/apps",
        headers=auth_headers,
        json={
            "project_id": project["id"],
            "name": "App One",
            "slug": "app-one",
            "deploy_mode": "platform_subdomain",
            "platform_subdomain": "app-one-x",
        },
    )

    apps = client.get(
        f"/v1/apps?project_id={project['id']}&deploy_mode=platform_subdomain",
        headers=auth_headers,
    )
    assert apps.status_code == 200
    assert len(apps.json()) == 1


def test_events_cursor_pagination_is_stable(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Ev", "slug": "org-ev"}).json()
    project = client.post(
        "/v1/projects",
        headers=auth_headers,
        json={"organization_id": org["id"], "name": "Proj Ev"},
    ).json()

    client.post(
        f"/v1/projects/{project['id']}/transitions",
        headers=auth_headers,
        json={"to_state": "discovery_active", "reason_code": "kickoff"},
    )
    client.post(
        f"/v1/projects/{project['id']}/transitions",
        headers=auth_headers,
        json={"to_state": "sow_drafting", "reason_code": "next"},
    )

    first = client.get(f"/v1/projects/{project['id']}/events?limit=1", headers=auth_headers)
    assert first.status_code == 200
    assert len(first.json()) == 1
    cursor = first.headers.get("X-Next-Cursor")
    assert cursor

    second = client.get(
        f"/v1/projects/{project['id']}/events?limit=1&cursor={cursor}",
        headers=auth_headers,
    )
    assert second.status_code == 200
    assert len(second.json()) == 1
    assert first.json()[0]["id"] != second.json()[0]["id"]


def test_idempotency_key_reuses_same_response_for_create_project(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Idem", "slug": "org-idem"}).json()
    headers = dict(auth_headers)
    headers["Idempotency-Key"] = "idem-proj-1"
    payload = {"organization_id": org["id"], "name": "Same Project"}

    first = client.post("/v1/projects", headers=headers, json=payload)
    second = client.post("/v1/projects", headers=headers, json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]

    listed = client.get(f"/v1/projects?organization_id={org['id']}", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1


def test_idempotency_key_rejects_different_payload(client, auth_headers):
    org = client.post("/v1/orgs", headers=auth_headers, json={"name": "Org Diff", "slug": "org-diff"}).json()
    headers = dict(auth_headers)
    headers["Idempotency-Key"] = "idem-proj-2"

    first = client.post(
        "/v1/projects",
        headers=headers,
        json={"organization_id": org["id"], "name": "Project A"},
    )
    second = client.post(
        "/v1/projects",
        headers=headers,
        json={"organization_id": org["id"], "name": "Project B"},
    )

    assert first.status_code == 200
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "idempotency_key_reused"


def test_invalid_cursor_returns_error(client, auth_headers):
    response = client.get("/v1/orgs?cursor=not-base64", headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_cursor"
