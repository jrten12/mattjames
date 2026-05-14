def test_client_portal_shell_renders(client):
    response = client.get("/portal")
    assert response.status_code == 200
    text = response.text
    assert "Client Portal" in text
    assert "How to use this page" in text
    assert "New Request" in text
    assert "My Requests" in text
    assert "Preview Review" in text
    assert "Submit Decision" in text
