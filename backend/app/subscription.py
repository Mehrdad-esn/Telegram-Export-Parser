"""Subscription plans and usage limits."""

from datetime import datetime, timezone
from typing import Dict, Optional

PLANS: Dict[str, Dict] = {
    "free": {
        "name": "رایگان",
        "name_en": "Free",
        "max_uploads_per_month": None,
        "max_exports_per_month": None,
        "max_file_size_mb": 10240,
        "max_chats": None,
        "filters_enabled": True,
        "formats": ["csv", "txt", "json", "md", "html", "xlsx", "excel"],
        "price_monthly": 0,
    },
    "pro": {
        "name": "حرفه‌ای",
        "name_en": "Pro",
        "max_uploads_per_month": None,
        "max_exports_per_month": None,
        "max_file_size_mb": 10240,
        "max_chats": None,
        "filters_enabled": True,
        "formats": ["csv", "txt", "json", "md", "html", "xlsx", "excel"],
        "price_monthly": 0,
    },
    "business": {
        "name": "سازمانی",
        "name_en": "Business",
        "max_uploads_per_month": None,
        "max_exports_per_month": None,
        "max_file_size_mb": 10240,
        "max_chats": None,
        "filters_enabled": True,
        "formats": ["csv", "txt", "json", "md", "html", "xlsx", "excel"],
        "price_monthly": 0,
    },
}


def get_plan_limits(plan: str) -> Dict:
    return PLANS.get(plan, PLANS["free"])


def reset_usage_if_needed(user) -> None:
    now = datetime.now(timezone.utc)
    if user.last_usage_reset is None or user.last_usage_reset.month != now.month or user.last_usage_reset.year != now.year:
        user.uploads_this_month = 0
        user.exports_this_month = 0
        user.last_usage_reset = now


def check_upload_allowed(user) -> Optional[str]:
    return None


def check_export_allowed(user, fmt: str) -> Optional[str]:
    return None


def get_usage_summary(user) -> Dict:
    reset_usage_if_needed(user)
    limits = get_plan_limits(user.plan or "free")
    return {
        "plan": user.plan or "free",
        "plan_name": limits["name"],
        "plan_name_en": limits["name_en"],
        "uploads_used": user.uploads_this_month,
        "uploads_limit": limits["max_uploads_per_month"],
        "exports_used": user.exports_this_month,
        "exports_limit": limits["max_exports_per_month"],
        "max_file_size_mb": limits["max_file_size_mb"],
        "subscription_status": user.subscription_status,
        "formats": limits["formats"],
    }
