"""Integration tests for the full export pipeline."""

import json
import tempfile
from pathlib import Path

from exporters import get_exporter
from stats import MessageStats
from filters import MessageFilter
from app import list_chat_names, process_chat
from telegram_to_text import format_message, build_id_index
from utils import extract_plain_text, extract_sender_name, coerce_to_str


def test_csv_exporter():
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])
    id_index = {str(m.get("id")): m for m in messages}

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
        tmp = Path(f.name)
    try:
        exporter = get_exporter("csv")(messages, id_index)
        exporter.export(tmp)
        content = tmp.read_text(encoding="utf-8")
        assert "sender" in content
        assert "علی" in content
    finally:
        tmp.unlink(missing_ok=True)


def test_filter_chained():
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])

    mf = MessageFilter(messages)
    mf.add_keyword_filter(["سلام"]).add_sender_filter(["علی"])
    filtered = mf.apply()
    assert len(filtered) >= 1
    for msg in filtered:
        assert extract_sender_name(msg) == "علی"
        assert "سلام" in extract_plain_text(msg.get("text"))


def test_stats():
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])

    stats = MessageStats(messages)
    assert stats.get_total_messages() >= 1
    assert stats.get_average_message_length() > 0
    top = stats.get_top_talkers(5)
    assert len(top) >= 1
    words = stats.get_word_frequency(5)
    assert len(words) >= 1


def test_format_message_with_reply():
    messages = [
        {"id": 1, "type": "message", "date": "2024-01-01T12:00:00", "from": "Alice", "text": "Hello!"},
        {"id": 2, "type": "message", "date": "2024-01-01T12:01:00", "from": "Bob", "text": "Hi!", "reply_to_message_id": 1},
    ]
    id_index = build_id_index(messages)
    formatted = format_message(messages[1], id_index)
    assert "Alice" in formatted
    assert "Hello" in formatted
    assert "↳" in formatted


def test_plain_text_export():
    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])
    id_index = {str(m.get("id")): m for m in messages}

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
        tmp = Path(f.name)
    try:
        exporter = get_exporter("txt")(messages, id_index)
        exporter.export(tmp)
        content = tmp.read_text(encoding="utf-8")
        assert "Telegram Chat Export" in content
        assert "علی" in content
    finally:
        tmp.unlink(missing_ok=True)
