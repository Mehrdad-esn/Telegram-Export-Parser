#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utility functions for Telegram export parser."""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional


def slugify(value: str, default: str = "chat") -> str:
    """Convert text to URL-safe slug."""
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_-]+", "-", value).strip("-")
    return value or default


def ensure_dir(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)


def unique_output_path(path: Path) -> Path:
    """Generate unique output path if file exists."""
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 2
    while True:
        candidate = parent / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def coerce_to_str(value: Any) -> str:
    """Convert any value to string intelligently."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, dict):
        for key in ("id", "user_id", "message_id", "value", "name", "title", "text"):
            if key in value:
                res = coerce_to_str(value.get(key))
                if res:
                    return res
        return ""
    if isinstance(value, list):
        items = [coerce_to_str(v) for v in value if coerce_to_str(v)]
        return " ".join(items).strip()
    return str(value)


def extract_plain_text(text_field: Any) -> str:
    """Extract plain text from nested text structures."""
    parts: List[str] = []

    def walk(node: Any) -> None:
        if node is None:
            return
        if isinstance(node, str):
            parts.append(node)
            return
        if isinstance(node, (int, float, bool)):
            parts.append(str(node))
            return
        if isinstance(node, list):
            for item in node:
                walk(item)
            return
        if isinstance(node, dict):
            if "text" in node:
                walk(node.get("text"))
                return
            for key in ("content", "value", "message", "caption"):
                if key in node:
                    walk(node.get(key))
                    return
            return
        parts.append(str(node))

    walk(text_field)
    text = "".join(parts)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def extract_sender_name(message: Dict[str, Any]) -> str:
    """Extract sender name from message."""
    name = coerce_to_str(message.get("from") or message.get(
        "actor") or message.get("author"))
    return name if name else "Unknown"


def extract_reply_id(message: Dict[str, Any]) -> Optional[str]:
    """Extract reply_to_message_id if exists."""
    value = message.get("reply_to_message_id")
    if value in (None, ""):
        return None
    return coerce_to_str(value)


def is_media_message(message: Dict[str, Any]) -> bool:
    """Check if message contains media."""
    media_keys = {"photo", "video", "sticker", "file",
                  "document", "audio", "voice", "animation", "media_type"}
    return any(key in message and message.get(key) for key in media_keys)


def extract_timestamp(message: Dict[str, Any]) -> str:
    """Extract and format timestamp."""
    ts = message.get("date", "")
    return ts.replace("T", " ") if ts else ""


def extract_message_id(message: Dict[str, Any]) -> str:
    """Extract message ID."""
    msg_id = message.get("id")
    return coerce_to_str(msg_id) if msg_id else ""
