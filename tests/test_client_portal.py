def test_client_portal_shell_renders(client):
    response = client.get("/portal")
    assert response.status_code == 200
    text = response.text
    assert "Client Portal" in text
    assert "AI Intake Assistant" in text
    assert "Start your AI intake" in text
    assert "My Requests" in text
    assert "Statement of Work" in text
    assert "Submit SOW decision" in text
