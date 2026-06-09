from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_process_json():
    sample = {
        "name": "Test Chat",
        "messages": [
            {"type": "message", "date": "2024-01-01T12:00:00", "from": "Alice", "text": "Hello", "id": 1}
        ],
    }
    resp = client.post("/api/process", json=sample)
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("processed") is True
    chats = body.get("chats") or []
    assert len(chats) == 1
    assert "Hello" in chats[0]["messages"][0]
