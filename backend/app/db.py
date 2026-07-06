"""Database engine and session management for backend app."""

import os
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

config = Config()
DATABASE_URL = os.getenv("DATABASE_URL", config.get_database_url())

connect_args = {}
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    if ":memory:" in DATABASE_URL:
        from sqlalchemy.pool import StaticPool
        engine_kwargs["poolclass"] = StaticPool

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


def migrate_schema():
    """Add missing columns to existing tables (SQLite-safe)."""
    inspector = inspect(engine)
    if "users" not in inspector.get_table_names():
        return
    existing = {col["name"] for col in inspector.get_columns("users")}
    new_columns = {
        "plan": "VARCHAR DEFAULT 'free'",
        "stripe_customer_id": "VARCHAR",
        "stripe_subscription_id": "VARCHAR",
        "subscription_status": "VARCHAR",
        "uploads_this_month": "INTEGER DEFAULT 0",
        "exports_this_month": "INTEGER DEFAULT 0",
        "last_usage_reset": "DATETIME",
    }
    with engine.connect() as conn:
        for col_name, col_def in new_columns.items():
            if col_name not in existing:
                conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_def}"))
        conn.commit()
