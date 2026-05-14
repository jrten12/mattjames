def test_metrics_endpoint_counts_requests(client, auth_headers):
    client.get("/health")
    client.get("/health")
    client.get("/v1/orgs", headers=auth_headers)

    metrics = client.get("/admin/metrics")
    assert metrics.status_code == 200
    body = metrics.json()["metrics"]
    assert body["request_total"] >= 3
    assert body["request_by_path"]["/health"] >= 2


def test_readyz_inmemory_mode(client):
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["storage"] == "inmemory"
