#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

try:
    import ijson  # type: ignore
    HAS_IJSON = True
except Exception:
    HAS_IJSON = False

try:
    from tqdm import tqdm  # type: ignore
    HAS_TQDM = True
except Exception:
    HAS_TQDM = False

from utils import (
    coerce_to_str,
    slugify,
    ensure_dir,
    unique_output_path,
    extract_plain_text,
    extract_sender_name,
    extract_reply_id,
    is_media_message,
)


# ----------------------------
# Core Formatter
# ----------------------------


def format_message(message: Dict[str, Any], id_index: Dict[str, Dict[str, Any]]) -> str:
    timestamp = message.get("date", "").replace("T", " ")
    sender = extract_sender_name(message)
    text = extract_plain_text(message.get("text")).strip()

    lines = [f"[{timestamp}] {sender}"]

    reply_id = extract_reply_id(message)
    if reply_id:
        parent = id_index.get(reply_id)
        if parent:
            parent_sender = extract_sender_name(parent)
            parent_text = extract_plain_text(parent.get("text")).strip()

            if not parent_text:
                parent_text = "[رسانه]"
            if len(parent_text) > 80:
                parent_text = parent_text[:80] + "..."

            lines.append(f"\u21b3 {parent_sender}: {parent_text}")

    if text:
        lines.append(text)
    elif is_media_message(message):
        lines.append("[رسانه]")

    return "\n".join(lines)


# ----------------------------
# Data Processing Engine
# ----------------------------


def iter_chats(json_path: Path) -> Iterator[Dict[str, Any]]:
    """هوشمندانه تشخیص می‌دهد فایل مربوط به کل اکانت است یا فقط یک چت"""
    if HAS_IJSON:
        try:
            found_in_list = False
            with json_path.open("rb") as f:
                for chat in ijson.items(f, "chats.list.item"):
                    found_in_list = True
                    yield chat

            if found_in_list:
                return

            with json_path.open("rb") as f:
                for root_obj in ijson.items(f, ""):
                    if isinstance(root_obj, dict) and "messages" in root_obj:
                        yield root_obj
            return
        except Exception:
            pass

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "messages" in data:
        yield data
    else:
        chats_root = data.get("chats", {})
        for chat in chats_root.get("list", []):
            yield chat


def build_id_index(messages: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    index = {}
    for msg in messages:
        msg_id = coerce_to_str(msg.get("id"))
        if msg_id:
            index[msg_id] = msg
    return index


def process_chat(chat: Dict[str, Any], output_dir: Path) -> None:
    chat_name = coerce_to_str(chat.get("name")) or "Unnamed chat"
    chat_slug = slugify(chat_name)

    messages = chat.get("messages", [])
    if not isinstance(messages, list):
        messages = []

    id_index = build_id_index(messages)
    ensure_dir(output_dir)

    txt_path = unique_output_path(output_dir / f"{chat_slug}.txt")

    iterator: Iterable[Dict[str, Any]] = messages
    if HAS_TQDM and len(messages) >= 200:
        iterator = tqdm(messages, desc=f"Processing {chat_name}", unit="msg")

    processed_count = 0
    with txt_path.open("w", encoding="utf-8") as out_file:
        for message in iterator:
            if not isinstance(message, dict):
                continue
            if message.get("type") != "message":
                continue

            formatted_msg = format_message(message, id_index)
            out_file.write(formatted_msg)
            out_file.write("\n\n")
            processed_count += 1

    print(f"✅ Chat '{chat_name}' processed successfully!")
    print(f"  ➜ Total messages: {processed_count}")
    print(f"  ➜ Output saved to: {txt_path}\n")


def list_chat_names(json_path: Path) -> List[str]:
    names = []
    for chat in iter_chats(json_path):
        names.append(coerce_to_str(chat.get("name")) or "(unnamed chat)")
    return names


# ----------------------------
# CLI (Command Line Interface)
# ----------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse Telegram JSON to LLM-Friendly Plain Text."
    )
    parser.add_argument(
        "--input", "-i", default="result.json", help="Path to result.json"
    )
    parser.add_argument(
        "--outdir", "-o", default="telegram_output", help="Output directory"
    )
    parser.add_argument("--chat", "-c", default=None, help="Exact chat name")
    parser.add_argument("--all-chats", action="store_true", help="Process all chats")
    args = parser.parse_args()

    json_path = Path(args.input)
    output_dir = Path(args.outdir)

    if not json_path.exists():
        print(f"❌ Error: Input file not found: {json_path}")
        sys.exit(1)

    available_chats = list_chat_names(json_path)
    if not available_chats:
        print("❌ Error: No chats found in the export.")
        sys.exit(1)

    if args.all_chats:
        print(f"🔍 Found {len(available_chats)} chats. Processing all...")
        for chat in iter_chats(json_path):
            if isinstance(chat, dict):
                process_chat(chat, output_dir)
        return

    target_chats = [args.chat] if args.chat else []

    if not target_chats:
        print("Available chats:")
        for idx, name in enumerate(available_chats, start=1):
            print(f"{idx:>3}. {name}")
        choice = input("\nType a chat name or number (default: 1): ").strip()
        if not choice:
            target_chats = [available_chats[0]]
        elif choice.isdigit() and 1 <= int(choice) <= len(available_chats):
            target_chats = [available_chats[int(choice) - 1]]
        elif choice in available_chats:
            target_chats = [choice]
        else:
            print(f"❌ Chat '{choice}' not found.")
            sys.exit(1)

    for chat in iter_chats(json_path):
        name = coerce_to_str(chat.get("name")) or "(unnamed chat)"
        if name in target_chats:
            process_chat(chat, output_dir)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🚫 Cancelled by user.")
        sys.exit(130)
