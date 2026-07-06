#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuration management for Telegram Export Parser."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration management."""

    DEFAULT_CONFIG = {
        "output_directory": "telegram_output",
        "default_export_format": "txt",
        "include_stats": False,
        "auto_translate": False,
        "translation_language": "en",
        "max_message_length": 0,  # 0 = unlimited
        "theme": "light",  # light or dark
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize config from file or use defaults."""
        self.config_path = Path(config_path) if config_path else Path("config.json")
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()

        if self.config_path.exists():
            self.load()

    def load(self) -> None:
        """Load config from JSON file."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                user_config = json.load(f)
            self.config.update(user_config)
        except Exception as e:
            print(f"⚠️  Warning: Could not load config: {e}")

    def save(self) -> None:
        """Save current config to JSON file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set config value."""
        self.config[key] = value

    def get_output_dir(self) -> Path:
        """Get output directory as Path."""
        return Path(self.get("output_directory", "telegram_output"))

    def get_export_format(self) -> str:
        """Get default export format."""
        return self.get("default_export_format", "txt")

    def get_database_url(self) -> str:
        """Get database URL configuration."""
        return self.get("database_url", "sqlite:///./telegram_export.db")

    def get_secret_key(self) -> str:
        """Get secret key configuration."""
        import secrets
        return self.get("secret_key", secrets.token_urlsafe(32))

    def __str__(self) -> str:
        """String representation."""
        return json.dumps(self.config, indent=2, ensure_ascii=False)


def create_default_config() -> None:
    """Create default config.json file."""
    config = Config()
    config.save()
    logging.info(f"✅ Config file created: {config.config_path}")


if __name__ == "__main__":
    create_default_config()
