def test_requires_api_key(client):
    response = client.get("/v1/orgs")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "missing_api_key"


def test_health_is_public(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
