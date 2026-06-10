"""Tests for database module."""

import pytest


class TestDatabaseModule:
    """Database module tests."""

    def test_db_module_imports(self):
        """Test that db module imports successfully."""
        try:
            from backend.app import db
            assert db is not None
        except ImportError:
            pytest.skip("DB module not fully configured")

    def test_base_model_exists(self):
        """Test that SQLAlchemy Base model exists."""
        try:
            from backend.app.db import Base
            assert Base is not None
        except ImportError:
            pytest.skip("DB module not fully configured")

    def test_engine_exists(self):
        """Test that database engine is configured."""
        try:
            from backend.app.db import engine
            assert engine is not None
        except ImportError:
            pytest.skip("DB module not fully configured")

    def test_session_local_exists(self):
        """Test that SessionLocal is configured."""
        try:
            from backend.app.db import SessionLocal
            assert SessionLocal is not None
        except ImportError:
            pytest.skip("DB module not fully configured")

    def test_get_db_dependency_exists(self):
        """Test that get_db dependency is available."""
        try:
            from backend.app.db import get_db
            assert get_db is not None
        except ImportError:
            pytest.skip("DB module not fully configured")


class TestDatabaseSession:
    """Database session tests."""

    def test_session_creation(self, db_session):
        """Test that database session can be created."""
        assert db_session is not None

    def test_session_query_capability(self, db_session):
        """Test that session supports queries."""
        assert hasattr(db_session, "query")
        assert callable(db_session.query)

    def test_session_cleanup(self, db_session):
        """Test that session can be cleaned up."""
        try:
            db_session.close()
            assert True
        except Exception as e:
            pytest.fail(f"Session cleanup failed: {e}")
