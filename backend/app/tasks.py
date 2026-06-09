"""Background tasks for the backend.

Tasks are registered on the Celery app defined in backend.worker.celery_app.
"""
from __future__ import annotations

from typing import Any, Dict

from backend.worker import celery_app

# Import processor lazily to avoid import cycles at module import time
from backend.app import processor


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
)
def process_export_task(self, payload: Any) -> Dict[str, Any]:
    """Process a parsed JSON export payload in the background.

    This wraps processor.process_export_from_payload and benefits from
    automatic retries with exponential backoff on failure.
    """
    return processor.process_export_from_payload(payload)
