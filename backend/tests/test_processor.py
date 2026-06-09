import json
from pathlib import Path

from backend.app import processor


def test_process_from_file():
    repo_root = Path(__file__).resolve().parents[2]
    test_file = repo_root / "test_data.json"

    result = processor.process_export_from_file(str(test_file))
    assert result.get("processed") is True

    chats = result.get("chats")
    assert isinstance(chats, list)
    names = [c.get("name") for c in chats]
    assert "Test Chat" in names

    test_chat = next(c for c in chats if c.get("name") == "Test Chat")
    # Ensure at least one formatted message exists and reply formatting is present
    assert any(isinstance(m, str) and m for m in test_chat.get("messages", []))
    assert any("↳" in m or "علی" in m for m in test_chat.get("messages", []))


def test_process_from_payload_idempotent():
    repo_root = Path(__file__).resolve().parents[2]
    test_file = repo_root / "test_data.json"
    payload = json.loads(test_file.read_text(encoding="utf-8"))

    r1 = processor.process_export_from_payload(payload)
    r2 = processor.process_export_from_payload(payload)
    assert r1 == r2
