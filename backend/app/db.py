"""Database engine and session management for backend app."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

config = Config()
DATABASE_URL = os.getenv("DATABASE_URL", config.get_database_url())

connect_args = {}
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    # For sqlite file-based DBs, ensure check_same_thread is False to allow multithreaded access.
    connect_args = {"check_same_thread": False}
    # For in-memory sqlite, use StaticPool so the database is preserved across connections.
    if ":memory:" in DATABASE_URL:
        from sqlalchemy.pool import StaticPool

        engine_kwargs["poolclass"] = StaticPool

# create engine and session factory
if connect_args or engine_kwargs:
    engine = create_engine(DATABASE_URL, connect_args=connect_args, **engine_kwargs)
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
