from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_signup_login_refresh():
    # Signup
    resp = client.post("/api/signup", json={"email": "user@example.com", "password": "secret"})
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["email"] == "user@example.com"

    # Login
    resp = client.post("/api/login", data={"username": "user@example.com", "password": "secret"})
    assert resp.status_code == 200, resp.text
    tokens = resp.json()
    assert "access_token" in tokens and "refresh_token" in tokens
    access = tokens["access_token"]

    # Me
    headers = {"Authorization": f"Bearer {access}"}
    resp = client.get("/api/me", headers=headers)
    assert resp.status_code == 200, resp.text
    me = resp.json()
    assert me["email"] == "user@example.com"

    # Refresh
    refresh = tokens["refresh_token"]
    resp = client.post("/api/refresh", json={"refresh_token": refresh})
    assert resp.status_code == 200, resp.text
    new_tokens = resp.json()
    assert "access_token" in new_tokens
