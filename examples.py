#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example: Advanced filtering and exporting with custom logic
"""

import json
from pathlib import Path
from filters import MessageFilter
from exporters import CSVExporter, HTMLExporter
from utils import ensure_dir, extract_sender_name


def example_basic_filter():
    """Example 1: Basic keyword filtering"""
    print("=" * 50)
    print("EXAMPLE 1: Keyword Filtering")
    print("=" * 50)

    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])

    # Filter messages containing "سلام"
    msg_filter = MessageFilter(messages)
    msg_filter.add_keyword_filter(["سلام"], mode="any")
    filtered = msg_filter.apply()

    print(f"Total messages: {len(messages)}")
    print(f"Messages with 'سلام': {len(filtered)}")
    print()


def example_date_range_filter():
    """Example 2: Date range filtering"""
    print("=" * 50)
    print("EXAMPLE 2: Date Range Filtering")
    print("=" * 50)

    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])

    # Filter messages from Jan 16
    msg_filter = MessageFilter(messages)
    msg_filter.add_date_range(start_date="2024-01-16", end_date="2024-01-16")
    filtered = msg_filter.apply()

    print(f"Total messages: {len(messages)}")
    print(f"Messages on 2024-01-16: {len(filtered)}")
    for msg in filtered:
        date = msg.get("date", "")
        sender = extract_sender_name(msg)
        print(f"  - {date} | {sender}")
    print()


def example_sender_filter():
    """Example 3: Filter by specific sender"""
    print("=" * 50)
    print("EXAMPLE 3: Filter by Sender")
    print("=" * 50)

    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])

    # Filter messages from علی
    msg_filter = MessageFilter(messages)
    msg_filter.add_sender_filter(["علی"])
    filtered = msg_filter.apply()

    print(f"Total messages: {len(messages)}")
    print(f"Messages from 'علی': {len(filtered)}")
    for msg in filtered:
        print(f"  - {msg.get('text', '').strip()[:50]}")
    print()


def example_chained_filters():
    """Example 4: Multiple filters chained"""
    print("=" * 50)
    print("EXAMPLE 4: Chained Filters")
    print("=" * 50)

    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])

    # Filter: messages from علی AND containing "سلام" AND after Jan 15
    msg_filter = MessageFilter(messages)
    msg_filter.add_sender_filter(["علی"]) \
              .add_keyword_filter(["سلام"]) \
              .add_date_range(start_date="2024-01-15")

    filtered = msg_filter.apply()

    print(f"Total messages: {len(messages)}")
    print(f"Filtered (from علی + 'سلام' + after 2024-01-15): {len(filtered)}")
    for msg in filtered:
        print(f"  ✓ {msg.get('text', '').strip()}")
    print()


def example_export_filtered_csv():
    """Example 5: Export filtered messages to CSV"""
    print("=" * 50)
    print("EXAMPLE 5: Export Filtered Messages")
    print("=" * 50)

    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])

    # Create filter
    msg_filter = MessageFilter(messages)
    msg_filter.add_keyword_filter(["سلام"])
    filtered_messages = msg_filter.apply()

    # Add back the type field for exporter
    for msg in filtered_messages:
        if "type" not in msg:
            msg["type"] = "message"

    # Export
    id_index = {str(m.get("id")): m for m in filtered_messages}
    exporter = CSVExporter(filtered_messages, id_index)

    output_dir = Path("examples_output")
    ensure_dir(output_dir)

    output_path = output_dir / "filtered_salam.csv"
    exporter.export(output_path)

    print(f"✅ Exported {len(filtered_messages)} filtered messages to:")
    print(f"   {output_path}")
    print()


def example_length_filter():
    """Example 6: Filter by message length"""
    print("=" * 50)
    print("EXAMPLE 6: Filter by Message Length")
    print("=" * 50)

    with open("test_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    chat = data["chats"]["list"][0]
    messages = chat.get("messages", [])

    # Filter messages longer than 20 characters
    msg_filter = MessageFilter(messages)
    msg_filter.add_length_filter(min_length=20)
    filtered = msg_filter.apply()

    print(f"Total messages: {len(messages)}")
    print(f"Messages longer than 20 chars: {len(filtered)}")
    for msg in filtered:
        text = msg.get("text", "").strip()
        print(f"  - ({len(text)} chars) {text[:40]}...")
    print()


if __name__ == "__main__":
    print("\n🎯 Advanced Filtering Examples\n")

    example_basic_filter()
    example_date_range_filter()
    example_sender_filter()
    example_chained_filters()
    example_length_filter()
    example_export_filtered_csv()

    print("=" * 50)
    print("✅ All examples completed!")
    print("=" * 50)
