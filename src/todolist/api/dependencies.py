"""
Dependency injection for FastAPI endpoints.
"""
from sqlalchemy.orm import Session
from todolist.database.connection import SessionLocal
from todolist.services.project_service import ProjectService
from todolist.services.task_service import TaskService
from todolist.repositories.project_repository import ProjectRepository
from todolist.repositories.task_repository import TaskRepository


def get_db() -> Session:
    """
    Database session dependency.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session) -> ProjectService:
    """
    Get ProjectService instance with repository.
    """
    repository = ProjectRepository(db)
    return ProjectService(repository)


def get_task_service(db: Session) -> TaskService:
    """
    Get TaskService instance with repository.
    """
    repository = TaskRepository(db)
    return TaskService(repository)
