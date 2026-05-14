def test_add_and_list_org_members(client, auth_headers):
    org = client.post(
        "/v1/orgs",
        headers=auth_headers,
        json={"name": "Org One", "slug": "org-one"},
    ).json()

    created = client.post(
        f"/v1/orgs/{org['id']}/members",
        headers=auth_headers,
        json={"user_id": "usr_001", "role": "client_admin"},
    )
    assert created.status_code == 200
    assert created.json()["user_id"] == "usr_001"

    listed = client.get(f"/v1/orgs/{org['id']}/members", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1
