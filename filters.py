#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Message filtering module."""

import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable

from utils import extract_plain_text, extract_sender_name, extract_timestamp


class MessageFilter:
    """Filter messages based on various criteria."""

    def __init__(self, messages: List[Dict[str, Any]]):
        self.messages = messages
        self.filters: List[Callable[[Dict], bool]] = []

    def add_date_range(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> "MessageFilter":
        """Filter by date range (YYYY-MM-DD format)."""
        def date_filter(msg: Dict) -> bool:
            msg_date = msg.get("date", "").split("T")[0] if msg.get("date") else ""
            if start_date and msg_date < start_date:
                return False
            if end_date and msg_date > end_date:
                return False
            return True
        self.filters.append(date_filter)
        return self

    def add_sender_filter(self, senders: List[str]) -> "MessageFilter":
        """Filter by sender names."""
        sender_set = set(senders)
        def sender_filter(msg: Dict) -> bool:
            return extract_sender_name(msg) in sender_set
        self.filters.append(sender_filter)
        return self

    def add_keyword_filter(self, keywords: List[str], mode: str = "any") -> "MessageFilter":
        """Filter by keywords (any or all)."""
        def keyword_filter(msg: Dict) -> bool:
            text = extract_plain_text(msg.get("text")).lower()
            keyword_matches = [kw.lower() in text for kw in keywords]
            if mode == "all":
                return all(keyword_matches)
            else:  # "any"
                return any(keyword_matches)
        self.filters.append(keyword_filter)
        return self

    def add_regex_filter(self, pattern: str) -> "MessageFilter":
        """Filter by regex pattern."""
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        def regex_filter(msg: Dict) -> bool:
            text = extract_plain_text(msg.get("text"))
            return compiled_pattern.search(text) is not None
        self.filters.append(regex_filter)
        return self

    def add_length_filter(self, min_length: Optional[int] = None, max_length: Optional[int] = None) -> "MessageFilter":
        """Filter by message length."""
        def length_filter(msg: Dict) -> bool:
            text_len = len(extract_plain_text(msg.get("text")))
            if min_length and text_len < min_length:
                return False
            if max_length and text_len > max_length:
                return False
            return True
        self.filters.append(length_filter)
        return self

    def add_has_media_filter(self, has_media: bool = True) -> "MessageFilter":
        """Filter messages with or without media."""
        def media_filter(msg: Dict) -> bool:
            media_keys = {"photo", "video", "sticker", "file",
                         "document", "audio", "voice", "animation"}
            has_media_actual = any(key in msg and msg.get(key) for key in media_keys)
            return has_media_actual == has_media
        self.filters.append(media_filter)
        return self

    def apply(self) -> List[Dict[str, Any]]:
        """Apply all filters to messages."""
        filtered = self.messages
        for filter_func in self.filters:
            filtered = [msg for msg in filtered if filter_func(msg)]
        return filtered

    def count_results(self) -> int:
        """Count messages after filtering."""
        return len(self.apply())
