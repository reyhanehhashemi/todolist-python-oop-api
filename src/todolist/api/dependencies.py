"""
FastAPI Dependency Injection.

This module provides dependency injection functions for:
- Database session management
- Service layer instantiation
- Request context handling
"""

from typing import Generator, Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

# Import از db package
from todolist.db.database import SessionLocal
from todolist.db.session import get_db_context

# Import services
from todolist.services.db_project_service import DBProjectService
from todolist.services.db_task_service import DBTaskService


# ============================================================================
# Database Session Dependencies
# ============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Provide database session as a dependency.

    Yields:
        Session: SQLAlchemy database session

    Note:
        - Session is automatically closed after request
        - Transactions are committed on success
        - Rollback happens on exception
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# Service Dependencies
# ============================================================================

def get_project_service(
    db: Session = Depends(get_db)
) -> DBProjectService:
    """
    Provide project service instance.

    Args:
        db: Database session (injected automatically)

    Returns:
        DBProjectService: Initialized project service
    """
    return DBProjectService(db)


def get_task_service(
    db: Session = Depends(get_db)
) -> DBTaskService:
    """
    Provide task service instance.

    Args:
        db: Database session (injected automatically)

    Returns:
        DBTaskService: Initialized task service
    """
    return DBTaskService(db)


# ============================================================================
# Type Aliases for Clean Annotations
# ============================================================================

DatabaseSession = Annotated[Session, Depends(get_db)]
"""Type alias for database session dependency."""

ProjectService = Annotated[DBProjectService, Depends(get_project_service)]
"""Type alias for project service dependency."""

TaskService = Annotated[DBTaskService, Depends(get_task_service)]
"""Type alias for task service dependency."""
