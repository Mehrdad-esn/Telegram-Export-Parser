import os
import pathlib

# Ensure test database and secret are set before importing the app
# Use in-memory SQLite to avoid file lock issues in CI/test environments
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ.setdefault("SECRET_KEY", "test-secret-key")

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def setup_function():
    db_path = pathlib.Path("backend/test_auth.db")
    try:
        if db_path.exists():
            db_path.unlink()
    except Exception:
        pass


def teardown_function():
    db_path = pathlib.Path("backend/test_auth.db")
    try:
        if db_path.exists():
            db_path.unlink()
    except Exception:
        pass


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
    print("DEBUG tokens:", tokens)

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
