def _seed_project(client, auth_headers):
    org = client.post(
        "/v1/orgs",
        headers=auth_headers,
        json={"name": "Gamma", "slug": "gamma"},
    ).json()
    project = client.post(
        "/v1/projects",
        headers=auth_headers,
        json={"organization_id": org["id"], "name": "Rev Cycle"},
    ).json()
    return org, project


def test_valid_transition_appends_event(client, auth_headers):
    _org, project = _seed_project(client, auth_headers)

    transitioned = client.post(
        f"/v1/projects/{project['id']}/transitions",
        headers=auth_headers,
        json={"to_state": "discovery_active", "reason_code": "kickoff", "metadata": {"source": "pm"}},
    )
    assert transitioned.status_code == 200
    assert transitioned.json()["current_state"] == "discovery_active"

    events = client.get(f"/v1/projects/{project['id']}/events", headers=auth_headers)
    assert events.status_code == 200
    payload = events.json()
    assert len(payload) == 1
    assert payload[0]["event_type"] == "state_transitioned"
    assert payload[0]["previous_state"] == "intake"
    assert payload[0]["new_state"] == "discovery_active"


def test_invalid_transition_returns_error(client, auth_headers):
    _org, project = _seed_project(client, auth_headers)
    response = client.post(
        f"/v1/projects/{project['id']}/transitions",
        headers=auth_headers,
        json={"to_state": "production_live", "reason_code": "skip"},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_transition"
