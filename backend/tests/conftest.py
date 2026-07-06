"""Shared fixtures for backend tests."""

import os
from pathlib import Path
import tempfile
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure backend module is importable
backend_root = Path(__file__).resolve().parents[1]
repo_root = backend_root.parent

# Set test database URL before any imports
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key")


@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    from backend.app.db import Base, engine
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def test_client(test_db):
    """Create FastAPI test client."""
    from backend.app.main import app
    return TestClient(app)


@pytest.fixture
def db_session(test_db):
    """Create a test database session."""
    from backend.app.db import SessionLocal
    db = SessionLocal()
    yield db
    db.close()
