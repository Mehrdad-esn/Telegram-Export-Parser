"""Backend processor module

Provides a small, synchronous API for processing Telegram export JSON either
from a file path or from an already-loaded payload. This wraps the core
parsing helpers implemented in telegram_to_text.py so the web backend can
call a stable interface.

Functions are designed to be pure and idempotent (they do not write files).
They remain synchronous for MVP but are suitable to be invoked from a
background worker (Celery/RQ) later.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

# Ensure repository root is importable so we can reuse parsing helpers.
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

# Try to import core helpers from telegram_to_text.
try:
    from telegram_to_text import iter_chats, build_id_index, format_message  # type: ignore
except Exception:
    # Fallback implementations
    from utils import coerce_to_str, extract_plain_text, extract_sender_name

    def iter_chats(json_path: Path):
        with json_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "messages" in data:
            yield data
        else:
            chats_root = data.get("chats", {})
            for chat in chats_root.get("list", []):
                yield chat

    def build_id_index(messages: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        index: Dict[str, Dict[str, Any]] = {}
        for msg in messages:
            if isinstance(msg, dict) and msg.get("id") is not None:
                index[str(msg.get("id"))] = msg
        return index

    def format_message(message: Dict[str, Any], id_index: Dict[str, Dict[str, Any]]) -> str:
        ts = message.get("date", "").replace("T", " ")
        sender = extract_sender_name(message)
        text = extract_plain_text(message.get("text"))
        return f"[{ts}] {sender}\n{text}"


def _process_chat(chat: Dict[str, Any]) -> Dict[str, Any]:
    """Process a single chat object (dict) and return a dict with name/messages."""
    chat_name = chat.get("name") or "Unnamed chat"
    messages = chat.get("messages") or []
    if not isinstance(messages, list):
        messages = []

    id_index = build_id_index(messages)

    formatted_messages: List[str] = []
    for m in messages:
        if not isinstance(m, dict) or m.get("type") != "message":
            continue
        try:
            fm = format_message(m, id_index)
        except Exception:
            # Best-effort fallback formatting
            ts = m.get("date", "").replace("T", " ")
            sender = m.get("from") or m.get("actor") or m.get("author") or "Unknown"
            text_field = m.get("text")
            if isinstance(text_field, str):
                text = text_field
            else:
                text = json.dumps(text_field, ensure_ascii=False) if text_field is not None else ""
            fm = f"[{ts}] {sender}\n{text}"
        formatted_messages.append(fm)

    return {"name": chat_name, "messages": formatted_messages}


def process_export_from_payload(payload: Any) -> Dict[str, Any]:
    """Process an already-loaded JSON payload (dict) and return processed chats.

    Accepts either a single chat object (contains "messages") or a full export
    root with "chats": {"list": [...] }.
    """
    if not isinstance(payload, dict):
        raise ValueError("payload must be a JSON object/dict")

    result: List[Dict[str, Any]] = []
    if "messages" in payload:
        result.append(_process_chat(payload))
    else:
        chats_root = payload.get("chats", {})
        for chat in chats_root.get("list", []):
            result.append(_process_chat(chat))

    return {"processed": True, "chats": result}


def process_export_from_file(file_path: str) -> Dict[str, Any]:
    """Process a JSON file on disk and return processed chats.

    This function intentionally does not write outputs and is idempotent: running
    it multiple times with the same input yields the same result.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")

    result: List[Dict[str, Any]] = []
    for chat in iter_chats(p):
        result.append(_process_chat(chat))

    return {"processed": True, "chats": result}
