#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Configuration management for Telegram Export Parser."""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Try to load .env file if it exists
try:
    from dotenv import load_dotenv
    ENV_SUPPORT = True
    # Load .env file from repo root
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    ENV_SUPPORT = False
    logging.debug("python-dotenv not installed; environment variables will not be loaded from .env file")


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
        # Start with defaults, then layer in environment variables
        self.config: Dict[str, Any] = self.DEFAULT_CONFIG.copy()
        self._load_from_environment()

        if self.config_path.exists():
            self.load()

    def _load_from_environment(self) -> None:
        """Load configuration values from environment variables."""
        # Application settings
        self.config["debug"] = os.getenv("DEBUG", "False").lower() == "true"
        self.config["environment"] = os.getenv("ENVIRONMENT", "development")
        self.config["log_level"] = os.getenv("LOG_LEVEL", "INFO")
        
        # File settings
        self.config["output_directory"] = os.getenv("EXPORT_DIRECTORY", self.DEFAULT_CONFIG["output_directory"])
        self.config["upload_directory"] = os.getenv("UPLOAD_DIRECTORY", "./uploads")
        self.config["max_upload_size_mb"] = int(os.getenv("MAX_UPLOAD_SIZE_MB", "100"))
        
        # Export settings
        self.config["default_export_format"] = os.getenv("DEFAULT_EXPORT_FORMAT", self.DEFAULT_CONFIG["default_export_format"])
        self.config["include_stats"] = os.getenv("ENABLE_STATS", "False").lower() == "true"
        self.config["auto_translate"] = os.getenv("ENABLE_AUTO_TRANSLATE", "False").lower() == "true"
        self.config["translation_language"] = os.getenv("TRANSLATION_LANGUAGE", self.DEFAULT_CONFIG["translation_language"])
        self.config["max_message_length"] = int(os.getenv("MAX_MESSAGE_LENGTH", "0"))
        
        # UI settings
        self.config["theme"] = os.getenv("THEME", self.DEFAULT_CONFIG["theme"])
        
        # Database settings (application-level storage)
        self.config["database_url"] = os.getenv("DATABASE_URL", "sqlite:///./telegram_export.db")
        
        # API settings
        self.config["secret_key"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
        self.config["backend_url"] = os.getenv("BACKEND_URL", "http://localhost:8000")
        self.config["frontend_url"] = os.getenv("FRONTEND_URL", "http://localhost:3000")
        self.config["api_base_url"] = os.getenv("API_BASE_URL", "http://localhost:8000/api")

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
        """Get database URL."""
        return self.get("database_url", "sqlite:///./telegram_export.db")

    def get_secret_key(self) -> str:
        """Get secret key for application."""
        return self.get("secret_key", "dev-secret-key-change-in-production")

    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get("debug", False)

    def get_environment(self) -> str:
        """Get current environment (development, staging, production)."""
        return self.get("environment", "development")

    def __str__(self) -> str:
        """String representation with sensitive data masked."""
        config_copy = self.config.copy()
        # Mask sensitive values in output
        sensitive_keys = ["secret_key", "stripe_api_key", "stripe_webhook_secret", 
                         "sentry_dsn", "openai_api_key", "email_password", "database_url"]
        for key in sensitive_keys:
            if key in config_copy and config_copy[key]:
                config_copy[key] = "***MASKED***"
        return json.dumps(config_copy, indent=2, ensure_ascii=False)


def create_default_config() -> None:
    """Create default config.json file."""
    config = Config()
    config.save()
    logging.info(f"✅ Config file created: {config.config_path}")


if __name__ == "__main__":
    create_default_config()
