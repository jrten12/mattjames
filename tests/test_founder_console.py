def test_founder_console_shell_renders(client):
    response = client.get("/founder")
    assert response.status_code == 200
    text = response.text
    assert "Founder Console" in text
    assert "Quick Start" in text
    assert "Refresh Queue" in text
    assert "Preview & Approval Panel" in text
    assert "Create Decision" in text
    assert "Releases Panel" in text
    assert "Create Release Record" in text
