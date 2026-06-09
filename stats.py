#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statistics and analysis module for Telegram messages."""

import re
import logging
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Tuple

from utils import extract_plain_text, extract_sender_name

logger = logging.getLogger(__name__)


class MessageStats:
    """Calculate statistics from messages."""

    def __init__(self, messages: List[Dict[str, Any]]):
        self.messages = [m for m in messages if m.get("type") == "message"]

    def get_total_messages(self) -> int:
        """Get total message count."""
        return len(self.messages)

    def get_messages_per_sender(self) -> Dict[str, int]:
        """Count messages by sender."""
        counts: Dict[str, int] = {}
        for msg in self.messages:
            sender = extract_sender_name(msg)
            counts[sender] = counts.get(sender, 0) + 1
        return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))

    def get_word_frequency(self, top_n: int = 20) -> List[Tuple[str, int]]:
        """Get most common words."""
        words: List[str] = []
        for msg in self.messages:
            text = extract_plain_text(msg.get("text")).lower()
            # Simple word splitting (can be improved with NLTK)
            words.extend(re.findall(r"\b\w+\b", text))

        word_counts = Counter(words)
        # Filter common stop words
        stop_words = {
            "و",
            "در",
            "به",
            "که",
            "این",
            "است",
            "را",
            "از",
            "برای",
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
        }
        filtered = {
            w: c for w, c in word_counts.items() if w not in stop_words and len(w) > 2
        }
        return sorted(filtered.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def get_daily_message_count(self) -> Dict[str, int]:
        """Get message count by day."""
        daily: Dict[str, int] = {}
        for msg in self.messages:
            date_str = msg.get("date", "")
            if date_str:
                day = date_str.split("T")[0]
                daily[day] = daily.get(day, 0) + 1
        return dict(sorted(daily.items()))

    def get_average_message_length(self) -> float:
        """Get average message length in characters."""
        if not self.messages:
            return 0.0
        total_length = sum(
            len(extract_plain_text(m.get("text"))) for m in self.messages
        )
        return round(total_length / len(self.messages), 2)

    def get_top_talkers(self, top_n: int = 10) -> List[Tuple[str, int]]:
        """Get top speakers by message count."""
        counts = self.get_messages_per_sender()
        return list(counts.items())[:top_n]

    def print_summary(self) -> None:
        """Print statistics summary using logging."""
        logger.info("\n📊 === CHAT STATISTICS ===")
        logger.info(f"Total messages: {self.get_total_messages()}")
        logger.info(
            f"Average message length: {self.get_average_message_length()} chars"
        )

        top_talkers = self.get_top_talkers(5)
        logger.info("\n👥 Top 5 Talkers:")
        for sender, count in top_talkers:
            logger.info(f"  • {sender}: {count} messages")

        top_words = self.get_word_frequency(10)
        logger.info("\n🔤 Top 10 Words:")
        for word, count in top_words:
            logger.info(f"  • {word}: {count}")

        daily_counts = self.get_daily_message_count()
        if daily_counts:
            avg_daily = sum(daily_counts.values()) / len(daily_counts)
            logger.info(f"\n📅 Messages per day: ~{avg_daily:.1f} (average)")
            logger.info(
                f"  Date range: {min(daily_counts.keys())} to {max(daily_counts.keys())}"
            )

        logger.info("")
