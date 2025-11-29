"""
Database base configuration.

This module provides the SQLAlchemy base class for all models.
Engine and Session are managed by db.database module.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.

    All SQLAlchemy models should inherit from this class.
    """
    pass


def init_db() -> None:
    """
    Initialize database by creating all tables.

    This function creates all tables defined in models
    that inherit from Base.

    Note:
        In production, use Alembic migrations instead.
        This is mainly for development and testing.
    """
    # Import models to register them with Base
    from . import db_project, db_task  # noqa: F401

    # Import engine from central location
    from ..db.database import engine

    # Create all tables
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """
    Drop all database tables.

    Warning:
        This will delete all data! Use only for testing.
    """
    # Import engine from central location
    from ..db.database import engine

    # Drop all tables
    Base.metadata.drop_all(bind=engine)
