"""
Dependency injection for FastAPI routes.
"""
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from todolist.db.database import SessionLocal
from todolist.services.project_service import ProjectService
from todolist.services.task_service import TaskService
from todolist.repositories.project_repository import ProjectRepository
from todolist.repositories.task_repository import TaskRepository


def get_db() -> Generator[Session, None, None]:
    """
    Get database session.

    Yields:
        Session: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session = Depends(get_db)):
    """
    Get project service instance.

    Args:
        db: Database session

    Returns:
        ProjectService: Project service instance
    """
    project_repository = ProjectRepository(db)
    return ProjectService(project_repository)


def get_task_service(db: Session = Depends(get_db)):
    """
    Get task service instance.

    Args:
        db: Database session

    Returns:
        TaskService: Task service instance
    """
    task_repository = TaskRepository(db)
    return TaskService(task_repository)
