"""
Session management utilities.

Provides context managers and helper functions for database sessions.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy.orm import Session

from .database import SessionLocal


def get_db() -> Session:
    """
    Create a new database session.

    Returns:
        SQLAlchemy Session instance

    Note:
        Caller is responsible for closing the session.
        Prefer using get_db_context() for automatic cleanup.
    """
    return SessionLocal()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Context manager for database sessions with automatic transaction management.

    Yields:
        SQLAlchemy Session instance

    Note:
        This automatically handles commit/rollback/close.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
