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

# Setup test database
TEST_DB_PATH = Path(tempfile.gettempdir()) / "test_telegram_export.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"


@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    # Ensure database is created
    from backend.app.db import Base, engine
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


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
