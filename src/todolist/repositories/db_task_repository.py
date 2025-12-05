"""
Database-backed task repository for data persistence.

This module provides PostgreSQL storage and retrieval operations
for Task entities using SQLAlchemy ORM.
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.db_task import DBTask, TaskStatus
from ..utils.exceptions import ResourceNotFoundError, LimitExceededError
from ..utils import get_tehran_now  # ✅ اضافه شد
from ..config import settings
from ..utils.timezone import get_tehran_now, convert_to_tehran_naive

class DBTaskRepository:
    """
    Repository for managing Task entities in PostgreSQL.

    This class provides CRUD operations for tasks and enforces
    business constraints like maximum task count.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize task repository with database session.

        Args:
            session: SQLAlchemy database session
        """
        self._session = session

    def _get_next_id(self) -> int:
        """
        Get the next available task ID by finding the first gap.

        Returns:
            Next available ID (smallest unused positive integer)
        """
        # Get all existing IDs sorted
        existing_ids = [
            row[0] for row in self._session.query(DBTask.id).order_by(DBTask.id).all()
        ]

        # Find first gap
        next_id = 1
        for existing_id in existing_ids:
            if existing_id == next_id:
                next_id += 1
            elif existing_id > next_id:
                break

        return next_id

    def add(
            self,
            title: str,
            project_id: int,
            description: str = "",
            status: str = TaskStatus.TODO.value,
            deadline: Optional[datetime] = None,
    ) -> DBTask:
        """Add a new task to the database."""
        # Check task limit
        if self.count() >= settings.max_number_of_task:
            raise LimitExceededError("Task", settings.max_number_of_task)

        # Get next available ID
        next_id = self._get_next_id()

        # ✅ تبدیل deadline به Tehran naive اگر aware است
        if deadline is not None:
            deadline = convert_to_tehran_naive(deadline)

        # Create new task
        task = DBTask(
            id=next_id,
            title=title,
            project_id=project_id,
            description=description,
            status=TaskStatus(status),
            deadline=deadline,  # ✅ حالا naive است
        )

        self._session.add(task)
        self._session.flush()
        return task

    def get_by_id(self, task_id: int) -> DBTask:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Task identifier

        Returns:
            Task entity

        Raises:
            ResourceNotFoundError: If task is not found
        """
        task = self._session.query(DBTask).filter(DBTask.id == task_id).first()
        if task is None:
            raise ResourceNotFoundError("Task", str(task_id))
        return task

    def get_all(self) -> list[DBTask]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks
        """
        return self._session.query(DBTask).order_by(DBTask.id).all()

    def get_by_project_id(self, project_id: int) -> list[DBTask]:
        """
        Retrieve all tasks belonging to a specific project.

        Args:
            project_id: Project identifier

        Returns:
            List of tasks in the project
        """
        return (
            self._session.query(DBTask)
            .filter(DBTask.project_id == project_id)
            .order_by(DBTask.id)
            .all()
        )

    def update(self, task: DBTask) -> DBTask:
        """
        Update an existing task.

        Args:
            task: Task entity with updated data

        Returns:
            Updated task

        Raises:
            ResourceNotFoundError: If task is not found
        """
        existing = self._session.query(DBTask).filter(DBTask.id == task.id).first()
        if existing is None:
            raise ResourceNotFoundError("Task", str(task.id))

        # ✅ اگر وضعیت به DONE تغییر کرد، closed_at رو ست کن
        if task.status == TaskStatus.DONE and existing.closed_at is None:
            task.closed_at = get_tehran_now()
        # ✅ اگر از DONE به غیر DONE تغییر کرد، closed_at رو پاک کن
        elif task.status != TaskStatus.DONE and existing.closed_at is not None:
            task.closed_at = None

        self._session.merge(task)
        self._session.flush()
        return task

    def delete(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id: Task identifier

        Raises:
            ResourceNotFoundError: If task is not found
        """
        task = self.get_by_id(task_id)
        self._session.delete(task)
        self._session.flush()

    def delete_by_project_id(self, project_id: int) -> int:
        """
        Delete all tasks belonging to a project (cascade delete).

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks deleted
        """
        count = (
            self._session.query(DBTask)
            .filter(DBTask.project_id == project_id)
            .count()
        )
        self._session.query(DBTask).filter(DBTask.project_id == project_id).delete()
        self._session.flush()
        return count

    def count(self) -> int:
        """
        Get total count of tasks.

        Returns:
            Number of tasks in database
        """
        return self._session.query(DBTask).count()

    def count_by_project_id(self, project_id: int) -> int:
        """
        Get count of tasks in a specific project.

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks in the project
        """
        return (
            self._session.query(DBTask)
            .filter(DBTask.project_id == project_id)
            .count()
        )

    def exists(self, task_id: int) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: Task identifier

        Returns:
            True if task exists, False otherwise
        """
        return self._session.query(DBTask).filter(DBTask.id == task_id).count() > 0

    def clear(self) -> None:
        """Remove all tasks from database (for testing purposes)."""
        self._session.query(DBTask).delete()
        self._session.flush()
