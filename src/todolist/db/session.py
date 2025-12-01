"""
Database session management.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# ✅ پیدا کردن ریشه پروژه (جایی که .env است)
# از مسیر فایل فعلی، 3 پوشه به بالا می‌رویم
current_file = Path(__file__)  # .../src/todolist/db/session.py
project_root = current_file.parent.parent.parent.parent  # .../todolist-python-oop-api

# ✅ مسیر فایل .env
env_path = project_root / ".env"

# ✅ بارگذاری متغیرهای محیطی
load_dotenv(dotenv_path=env_path)

# خواندن DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        f"DATABASE_URL environment variable is not set!\n"
        f"Current directory: {os.getcwd()}\n"
        f"Project root: {project_root}\n"
        f".env path: {env_path}\n"
        f".env exists: {env_path.exists()}"
    )

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DB_ECHO", "False").lower() == "true",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for ORM models
Base = declarative_base()


def get_db():
    """
    Get database session.

    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
