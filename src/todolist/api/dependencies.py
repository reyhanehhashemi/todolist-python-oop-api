"""
FastAPI dependencies.
"""

from typing import Generator
from todolist.db.session import SessionLocal
from todolist.services.project_service import DBProjectService
from todolist.services.task_service import DBTaskService
from todolist.repositories.project_repository import ProjectRepository
from todolist.repositories.task_repository import TaskRepository


def get_db() -> Generator:
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


def get_project_service() -> DBProjectService:
    """
    Get project service instance.

    Returns:
        Project service
    """
    db = next(get_db())
    repository = ProjectRepository(db)
    return DBProjectService(repository)


def get_task_service() -> DBTaskService:
    """
    Get task service instance.

    Returns:
        Task service
    """
    db = next(get_db())
    repository = TaskRepository(db)
    return DBTaskService(repository)
