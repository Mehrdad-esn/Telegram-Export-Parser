#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Advanced Telegram Export Parser - Main Application."""

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
    ensure_dir,
    unique_output_path,
    extract_plain_text,
    extract_sender_name,
)
from stats import MessageStats
from filters import MessageFilter
from exporters import get_exporter

import logging
import builtins

# Configure logging for CLI
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("telegram_export_parser")


# Redirect prints to logger.info for consistent logging
def _print_to_logger(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    msg = sep.join(map(str, args))
    if end != "\n":
        msg += end
    logger.info(msg)


builtins.print = _print_to_logger


# ----------------------------
# Core Data Processing
# ----------------------------


def iter_chats(json_path: Path) -> Iterator[Dict[str, Any]]:
    """Intelligently detect if file is full export or single chat."""
    if HAS_IJSON:
        try:
            found_in_list = False
            with json_path.open("rb") as f:
                for chat in ijson.items(f, "chats.list.item"):
                    found_in_list = True
                    yield chat

            if found_in_list:
                return

            # If not in list, file is single chat export
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
    """Build index of messages by ID for reply tracking."""
    index = {}
    for msg in messages:
        msg_id = coerce_to_str(msg.get("id"))
        if msg_id:
            index[msg_id] = msg
    return index


def format_message_with_reply(
    message: Dict[str, Any], id_index: Dict[str, Dict[str, Any]]
) -> str:
    """Format message with reply context (plain text format)."""
    timestamp = message.get("date", "").replace("T", " ")
    sender = extract_sender_name(message)
    text = extract_plain_text(message.get("text")).strip()

    lines = [f"[{timestamp}] {sender}"]

    reply_id = message.get("reply_to_message_id")
    if reply_id:
        parent = id_index.get(str(reply_id))
        if parent:
            parent_sender = extract_sender_name(parent)
            parent_text = extract_plain_text(parent.get("text")).strip()

            if not parent_text:
                parent_text = "[رسانه]"

            if len(parent_text) > 80:
                parent_text = parent_text[:80] + "..."

            lines.append(f"↳ {parent_sender}: {parent_text}")

    media_keys = {
        "photo",
        "video",
        "sticker",
        "file",
        "document",
        "audio",
        "voice",
        "animation",
        "media_type",
    }
    has_media = any(key in message and message.get(key) for key in media_keys)

    if text:
        lines.append(text)
    elif has_media:
        lines.append("[رسانه]")

    return "\n".join(lines)


def list_chat_names(json_path: Path) -> List[str]:
    """List all available chat names."""
    names = []
    for chat in iter_chats(json_path):
        names.append(coerce_to_str(chat.get("name")) or "(unnamed chat)")
    return names


# ----------------------------
# Processing Functions
# ----------------------------


def process_chat(
    chat: Dict[str, Any],
    output_dir: Path,
    export_format: str = "txt",
    stats: bool = False,
    show_stats_only: bool = False,
) -> None:
    """Process single chat and export."""
    chat_name = coerce_to_str(chat.get("name")) or "Unnamed chat"
    messages = chat.get("messages", [])
    if not isinstance(messages, list):
        messages = []

    id_index = build_id_index(messages)
    ensure_dir(output_dir)

    # Filter to actual messages
    messages = [m for m in messages if m.get("type") == "message"]

    if show_stats_only:
        stats_obj = MessageStats(chat.get("messages", []))
        stats_obj.print_summary()
        return

    # Export messages
    if export_format == "txt":
        txt_path = unique_output_path(
            output_dir / f"{coerce_to_str(chat.get('name') or 'chat')}.txt"
        )

        iterator: Iterable[Dict[str, Any]] = messages
        if HAS_TQDM and len(messages) >= 200:
            iterator = tqdm(messages, desc=f"Processing {chat_name}", unit="msg")

        with txt_path.open("w", encoding="utf-8") as out_file:
            for message in iterator:
                if not isinstance(message, dict):
                    continue
                formatted_msg = format_message_with_reply(message, id_index)
                out_file.write(formatted_msg)
                out_file.write("\n\n")

        print(f"✅ Chat '{chat_name}' exported!")
        print(f"  ➜ Format: TXT ({len(messages)} messages)")
        print(f"  ➜ Output: {txt_path}\n")

    else:
        # Use exporters module
        from utils import extract_timestamp

        exporter_class = get_exporter(export_format)
        exporter = exporter_class(chat.get("messages", []), id_index)

        file_ext = "xlsx" if export_format in ["excel", "xlsx"] else export_format
        output_path = unique_output_path(
            output_dir / f"{coerce_to_str(chat.get('name') or 'chat')}.{file_ext}"
        )

        exporter.export(output_path)
        print(f"✅ Chat '{chat_name}' exported!")
        print(f"  ➜ Format: {export_format.upper()} ({len(messages)} messages)")
        print(f"  ➜ Output: {output_path}\n")

    # Print statistics if requested
    if stats:
        stats_obj = MessageStats(chat.get("messages", []))
        stats_obj.print_summary()


# ----------------------------
# CLI
# ----------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Advanced Telegram Export Parser - Extract & Analyze Chats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app.py -i result.json                    # Interactive mode
  python app.py -i result.json -c "John" -o out   # Export specific chat
  python app.py -i result.json --all-chats        # Export all chats
  python app.py -i result.json --format csv       # Export as CSV
  python app.py -i result.json --stats            # Show statistics
  python app.py -i result.json --stats-only       # Only show stats, no export
        """,
    )

    parser.add_argument(
        "-i", "--input", default="result.json", help="Path to Telegram export JSON file"
    )
    parser.add_argument(
        "-o", "--outdir", default="telegram_output", help="Output directory"
    )
    parser.add_argument("-c", "--chat", default=None, help="Exact chat name to export")
    parser.add_argument("--all-chats", action="store_true", help="Export all chats")
    parser.add_argument(
        "--format",
        default="txt",
        choices=["txt", "csv", "json", "md", "html", "xlsx"],
        help="Export format (default: txt)",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Show statistics after export"
    )
    parser.add_argument(
        "--stats-only", action="store_true", help="Show statistics without exporting"
    )

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
        print(f"🔍 Found {len(available_chats)} chats. Processing all...\n")
        for chat in iter_chats(json_path):
            if isinstance(chat, dict):
                process_chat(chat, output_dir, args.format, args.stats, args.stats_only)
        return

    target_chats = [args.chat] if args.chat else []

    if not target_chats:
        print("📋 Available chats:")
        for idx, name in enumerate(available_chats, start=1):
            print(f"  {idx:>3}. {name}")
        choice = input("\nSelect chat (name or number, default: 1): ").strip()
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
            process_chat(chat, output_dir, args.format, args.stats, args.stats_only)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🚫 Cancelled by user.")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
