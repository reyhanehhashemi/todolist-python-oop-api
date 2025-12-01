"""
Task service for business logic.

This module provides high-level operations for task management,
coordinating between repositories and enforcing business rules.
"""

from typing import Optional
from datetime import datetime
from ..models.task import Task, TaskStatus
from ..repositories.task_repository import TaskRepository
from ..utils.exceptions import ResourceNotFoundError, ValidationError


class TaskService:
    """
    Service layer for task management operations.

    This class provides business logic for creating, updating,
    and managing tasks.
    """

    def __init__(self, task_repository: TaskRepository) -> None:
        """
        Initialize task service.

        Args:
            task_repository: Repository for task persistence
        """
        self._task_repo = task_repository

    def create_task(
        self,
        title: str,
        project_id: int,
        description: str = "",
        status: str = TaskStatus.TODO.value,
        deadline: Optional[datetime] = None,
    ) -> Task:
        """
        Create a new task.

        Args:
            title: Task title
            project_id: ID of parent project
            description: Task description (optional)
            status: Initial status (default: TODO)
            deadline: Task deadline (optional)

        Returns:
            Created task

        Raises:
            ValidationError: If validation fails
            LimitExceededError: If task limit is reached
        """
        task = Task(
            title=title,
            project_id=project_id,
            description=description,
            status=status,
            deadline=deadline,
        )

        return self._task_repo.add(task)

    def get_task(self, task_id: int) -> Task:
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

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks
        """
        return self._task_repo.get_all()

    def get_tasks_by_project(self, project_id: int) -> list[Task]:
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
    ) -> Task:
        """
        Update task details.

        Args:
            task_id: Task identifier
            title: New title (optional)
            description: New description (optional)
            deadline: New deadline (optional)

        Returns:
            Updated task

        Raises:
            ResourceNotFoundError: If task not found
            ValidationError: If validation fails
        """
        task = self._task_repo.get_by_id(task_id)
        task.update_details(title=title, description=description, deadline=deadline)
        return self._task_repo.update(task)

    def update_task_status(self, task_id: int, new_status: str) -> Task:
        """
        Update task status.

        Args:
            task_id: Task identifier
            new_status: New status value

        Returns:
            Updated task

        Raises:
            ResourceNotFoundError: If task not found
            ValidationError: If status is invalid
        """
        task = self._task_repo.get_by_id(task_id)
        task.update_status(new_status)
        return self._task_repo.update(task)

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task.

        Args:
            task_id: Task identifier

        Raises:
            ResourceNotFoundError: If task not found
        """
        self._task_repo.delete(task_id)

    def delete_tasks_by_project(self, project_id: int) -> int:
        """
        Delete all tasks belonging to a project (cascade delete).

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks deleted
        """
        return self._task_repo.delete_by_project_id(project_id)

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

    def get_tasks_by_status(self, status: str) -> list[Task]:
        """
        Get all tasks with a specific status.

        Args:
            status: Status to filter by

        Returns:
            List of tasks with the given status

        Raises:
            ValidationError: If status is invalid
        """
        from ..utils.validators import validate_status

        validate_status(status, TaskStatus.values())

        return [task for task in self._task_repo.get_all() if task.status == status]


    def auto_close_overdue_tasks(self) -> int:
        """
        Automatically close overdue tasks.

        Tasks are closed if:
        - deadline < now
        - status != DONE

        Returns:
            Number of tasks closed
        """
        from datetime import datetime

        all_tasks = self._task_repo.get_all()
        closed_count = 0

        now = datetime.now()

        for task in all_tasks:
            # Skip if no deadline
            if task.deadline is None:
                continue

            # Skip if already DONE
            if task.status == TaskStatus.DONE.value:
                continue

            # Check if overdue
            if task.deadline < now:
                task.update_status(TaskStatus.DONE.value)
                self._task_repo.update(task)
                closed_count += 1

        return closed_count

