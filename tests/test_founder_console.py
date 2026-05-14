def test_founder_console_shell_renders(client):
    response = client.get("/founder")
    assert response.status_code == 200
    text = response.text
    assert "Founder Console - Intake Queue" in text
    assert "Refresh Queue" in text
    assert "Preview Builds" in text
