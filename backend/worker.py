"""Celery application for background processing tasks.

Broker and result backend are read from the REDIS_URL environment variable.
This module creates a Celery instance named `celery_app` that other modules
(e.g., backend.app.tasks) can import and use to register tasks.

Notes:
- For production consider using a dedicated persistent result backend
  (e.g., database via django-celery-results or a dedicated Redis DB index).
- Configure broker/result URLs via REDIS_URL env var (set in docker-compose).
"""
from __future__ import annotations

import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Create Celery application
celery_app = Celery("telegram_export", broker=REDIS_URL, backend=REDIS_URL)

# Basic recommended configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    result_expires=3600,  # seconds
    task_default_retry_delay=30,  # default retry delay in seconds
    task_annotations={"*": {"max_retries": 3}},
)

# Import tasks so they are registered when the worker starts.
# Keep import in a try/except so importing this module in contexts where
# tasks may be unavailable does not crash the process.
try:
    import backend.app.tasks  # noqa: F401
except Exception as exc:  # pragma: no cover - defensive import
    print("Could not import backend.app.tasks:", exc)
