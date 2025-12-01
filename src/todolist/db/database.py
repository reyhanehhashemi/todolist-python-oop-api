"""
Database engine and session factory.

This is the ONLY place where engine and SessionLocal are defined.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ..config.settings import settings

# ✅ Create engine (تنها جایی که engine ساخته میشه)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


# Enable foreign key constraints for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable foreign key constraints for SQLite."""
    if 'sqlite' in str(dbapi_conn):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# ✅ Session factory (تنها جایی که SessionLocal ساخته میشه)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db() -> None:
    """Initialize database by creating all tables."""
    from ..models.db_base import Base
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Drop all database tables (testing only)."""
    from ..models.db_base import Base
    Base.metadata.drop_all(bind=engine)
