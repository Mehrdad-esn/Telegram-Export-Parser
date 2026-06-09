"""
Monitoring module for Sentry error tracking and Prometheus metrics.

This module provides:
- Sentry SDK initialization with error tracking and performance monitoring
- Prometheus metrics endpoint for system and application metrics
- Health check and readiness status
"""

import os
import logging
from typing import Optional

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

logger = logging.getLogger(__name__)

# Sentry initialization
SENTRY_DSN = os.getenv("SENTRY_DSN")


def init_sentry(dsn: Optional[str] = None) -> bool:
    """
    Initialize Sentry SDK for error tracking and performance monitoring.
    
    Args:
        dsn: Sentry DSN. If None, will use SENTRY_DSN environment variable.
    
    Returns:
        True if Sentry was initialized, False if DSN is not available.
    
    Note:
        - Requires sentry-sdk package
        - Performance monitoring is enabled with 10% sample rate in production
        - Django/Flask integration is skipped if not using those frameworks
    """
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        
        sentry_url = dsn or SENTRY_DSN
        
        if not sentry_url:
            logger.info("SENTRY_DSN not configured; error tracking disabled")
            return False
        
        sentry_sdk.init(
            dsn=sentry_url,
            traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
            profiles_sample_rate=0.1,
            integrations=[
                FastApiIntegration(),
            ],
            environment=os.getenv("ENV", "development"),
            release=os.getenv("APP_VERSION", "unknown"),
            enable_tracing=True,
        )
        
        logger.info("Sentry initialized for error tracking and performance monitoring")
        return True
    
    except ImportError:
        logger.warning("sentry-sdk not installed; error tracking disabled")
        return False
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {e}")
        return False


# Prometheus metrics
def _build_metrics():
    """Create Prometheus metric definitions."""
    return {
        # Counter: Total requests by endpoint and method
        "requests_total": Counter(
            "http_requests_total",
            "Total HTTP requests",
            ["method", "endpoint", "status"],
        ),
        # Histogram: Request latency in seconds
        "request_duration_seconds": Histogram(
            "http_request_duration_seconds",
            "HTTP request latency in seconds",
            ["method", "endpoint", "status"],
            buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
        ),
        # Counter: Exceptions raised
        "exceptions_total": Counter(
            "exceptions_total",
            "Total exceptions raised",
            ["exception_type"],
        ),
        # Gauge: Active requests
        "requests_in_progress": Gauge(
            "http_requests_in_progress",
            "HTTP requests in progress",
        ),
        # Counter: Chat processing operations
        "chat_processing_total": Counter(
            "chat_processing_total",
            "Total chat processing operations",
            ["status"],  # success, failure
        ),
        # Histogram: Chat processing duration
        "chat_processing_duration_seconds": Histogram(
            "chat_processing_duration_seconds",
            "Chat processing duration in seconds",
            ["status"],
            buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0),
        ),
    }


METRICS = _build_metrics()


def get_metrics_text() -> str:
    """
    Generate Prometheus metrics output.
    
    Returns:
        Prometheus exposition format metrics as string.
    """
    return generate_latest().decode("utf-8")


def get_metrics_content_type() -> str:
    """Get the content type for Prometheus metrics response."""
    return CONTENT_TYPE_LATEST.decode("utf-8")


# Utility functions for middleware and handlers
def record_request(method: str, endpoint: str, status_code: int, duration: float):
    """
    Record HTTP request metrics.
    
    Args:
        method: HTTP method (GET, POST, etc.)
        endpoint: Request endpoint/path
        status_code: HTTP response status code
        duration: Request duration in seconds
    """
    METRICS["requests_total"].labels(method=method, endpoint=endpoint, status=status_code).inc()
    METRICS["request_duration_seconds"].labels(method=method, endpoint=endpoint, status=status_code).observe(duration)


def record_exception(exc_type: str):
    """Record exception metrics."""
    METRICS["exceptions_total"].labels(exception_type=exc_type).inc()


def increment_in_progress():
    """Increment active requests gauge."""
    METRICS["requests_in_progress"].inc()


def decrement_in_progress():
    """Decrement active requests gauge."""
    METRICS["requests_in_progress"].dec()


def record_chat_processing(success: bool, duration: float):
    """
    Record chat processing metrics.
    
    Args:
        success: Whether processing succeeded
        duration: Processing duration in seconds
    """
    status = "success" if success else "failure"
    METRICS["chat_processing_total"].labels(status=status).inc()
    METRICS["chat_processing_duration_seconds"].labels(status=status).observe(duration)
