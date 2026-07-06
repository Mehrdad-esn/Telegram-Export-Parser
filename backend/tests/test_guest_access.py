from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_guest_access_chats_endpoint():
    # Make request without Authorization header
    resp = client.get("/api/web/chats/non-existent-id")
    # Should be 404 (Not Found) because the file doesn't exist,
    # but NOT 401 (Unauthorized).
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Upload not found or expired"


def test_guest_access_upload_endpoint():
    # Try uploading a non-json file as guest
    files = {"file": ("test.txt", b"not-json-content", "text/plain")}
    resp = client.post("/api/web/upload", files=files)
    # Should return 400 (Only JSON files are allowed)
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Only JSON files are allowed"
