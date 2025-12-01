"""
Database-backed task service for business logic.

This module provides high-level operations for task management
using database repositories.
"""

from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.task import Task, TaskStatus
from ..models.db_task import DBTask
from ..repositories.db_task_repository import DBTaskRepository
from ..repositories.db_project_repository import DBProjectRepository
from ..utils.exceptions import (
    ResourceNotFoundError,
    ValidationError,
)


class DBTaskService:
    """
    Service layer for task management with database persistence.

    This class provides business logic for creating, updating,
    and managing tasks using PostgreSQL storage.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize task service with database session.

        Args:
            session: SQLAlchemy database session
        """
        self._task_repo = DBTaskRepository(session)
        self._project_repo = DBProjectRepository(session)
        self._session = session

    def create_task(
            self,
            title: str,
            project_id: int,
            description: str = "",
            status: str = TaskStatus.TODO.value,
            deadline: Optional[datetime] = None,
    ) -> DBTask:
        """
        Create a new task.

        Args:
            title: Task title (max 30 words)
            project_id: ID of parent project
            description: Task description (max 150 words, optional)
            status: Initial status (default: TODO)
            deadline: Task deadline (optional)

        Returns:
            Created task

        Raises:
            ValidationError: If validation fails
            ResourceNotFoundError: If project not found
            LimitExceededError: If task limit is reached
        """
        # Verify project exists
        if not self._project_repo.exists(project_id):
            raise ResourceNotFoundError("Project", str(project_id))

        # ✅ Repository خودش object میسازه
        created_task = self._task_repo.add(
            title=title,
            project_id=project_id,
            description=description,
            status=status,
            deadline=deadline
        )
        self._session.commit()
        return created_task

    def get_task(self, task_id: int) -> DBTask:
        """
        Retrieve a task by ID.

        Args:
            task_id: Task identifier

        Returns:
            Task entity

        Raises:
            ResourceNotFoundError: If task not found
        """
        return self._task_repo.get_by_id(task_id)

    def get_all_tasks(self) -> list[DBTask]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks
        """
        return self._task_repo.get_all()

    def get_tasks_by_project(self, project_id: int) -> list[DBTask]:
        """
        Retrieve all tasks for a specific project.

        Args:
            project_id: Project identifier

        Returns:
            List of tasks in the project
        """
        return self._task_repo.get_by_project_id(project_id)

    def update_task(
            self,
            task_id: int,
            title: Optional[str] = None,
            description: Optional[str] = None,
            deadline: Optional[datetime] = None,
    ) -> DBTask:
        """
        Update task details.

        Args:
            task_id: Task identifier
            title: New title (optional, max 30 words)
            description: New description (optional, max 150 words)
            deadline: New deadline (optional)

        Returns:
            Updated task

        Raises:
            ResourceNotFoundError: If task not found
            ValidationError: If validation fails
        """
        # Get existing task
        task = self._task_repo.get_by_id(task_id)

        # Update fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if deadline is not None:
            task.deadline = deadline

        # Persist changes
        updated_task = self._task_repo.update(task)
        self._session.commit()
        return updated_task

    def update_task_status(self, task_id: int, new_status: str) -> DBTask:
        """
        Update task status.

        Args:
            task_id: Task identifier
            new_status: New status value (TODO/DOING/DONE)

        Returns:
            Updated task

        Raises:
            ResourceNotFoundError: If task not found
            ValidationError: If status is invalid
        """
        # Validate status
        from ..utils.validators import validate_status
        validate_status(new_status, TaskStatus.values())

        # Get existing task
        task = self._task_repo.get_by_id(task_id)

        # Update status
        task.status = TaskStatus(new_status)

        # Persist changes
        updated_task = self._task_repo.update(task)
        self._session.commit()
        return updated_task

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task.

        Args:
            task_id: Task identifier

        Raises:
            ResourceNotFoundError: If task not found
        """
        self._task_repo.delete(task_id)
        self._session.commit()

    def delete_tasks_by_project(self, project_id: int) -> int:
        """
        Delete all tasks belonging to a project (cascade delete).

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks deleted
        """
        count = self._task_repo.delete_by_project_id(project_id)
        self._session.commit()
        return count

    def count_tasks(self) -> int:
        """
        Get total task count.

        Returns:
            Number of tasks
        """
        return self._task_repo.count()

    def count_tasks_by_project(self, project_id: int) -> int:
        """
        Get task count for a specific project.

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks in project
        """
        return self._task_repo.count_by_project_id(project_id)

    def get_tasks_by_status(self, status: str) -> list[DBTask]:
        """
        Get all tasks with a specific status.

        Args:
            status: Status to filter by (TODO/DOING/DONE)

        Returns:
            List of tasks with the given status

        Raises:
            ValidationError: If status is invalid
        """
        from ..utils.validators import validate_status

        # Validate status
        validate_status(status, TaskStatus.values())

        # Get all tasks and filter by status
        all_tasks = self._task_repo.get_all()
        return [task for task in all_tasks if task.status.value == status]

    def commit(self) -> None:
        """Commit the current database transaction."""
        self._session.commit()

    def rollback(self) -> None:
        """Rollback the current database transaction."""
        self._session.rollback()

    def auto_close_overdue_tasks(self) -> int:
        """
        Automatically close overdue tasks.

        Tasks are closed if:
        - deadline < now (in local timezone)
        - status != DONE

        Returns:
            Number of tasks closed
        """
        from datetime import datetime

        # ✅ استفاده از تایم محلی (نه UTC)
        now = datetime.now()

        all_tasks = self._task_repo.get_all()

        print(f"\n=== Auto-Close Debug Info ===")
        print(f"Current time (Local): {now}")
        print(f"Total tasks in DB: {len(all_tasks)}")

        closed_count = 0

        for task in all_tasks:
            # Skip tasks without deadline
            if task.deadline is None:
                continue

            # Get status as string (مقاوم در برابر Enum/String)
            if isinstance(task.status, str):
                status_value = task.status
            elif hasattr(task.status, 'value'):
                status_value = task.status.value
            else:
                status_value = str(task.status)

            # Skip already DONE tasks
            if status_value == TaskStatus.DONE.value:
                continue

            # ✅ تبدیل deadline به naive اگر aware است
            deadline = task.deadline
            if deadline.tzinfo is not None:
                # تبدیل به تایم محلی
                deadline = deadline.replace(tzinfo=None)

            print(f"Task {task.id}: deadline={deadline}, now={now}, overdue={deadline < now}")

            # Check if overdue
            if deadline < now:
                # Update to DONE
                task.status = TaskStatus.DONE  # ✅ نه .value
                task.closed_at = now  # ✅ نه now()

                # Save changes
                self._task_repo.update(task)
                closed_count += 1
                print(f"  -> Closed task {task.id}")

        # Commit all changes
        self._session.commit()

        print(f"Total closed: {closed_count}")
        return closed_count
