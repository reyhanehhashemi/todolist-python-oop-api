"""
Task repository for data persistence.

This module provides in-memory storage and retrieval operations
for Task entities.
"""

from typing import Optional
from ..models.task import Task
from ..utils.exceptions import ResourceNotFoundError, LimitExceededError
from ..config import settings


class TaskRepository:
    """
    Repository for managing Task entities in memory.

    This class provides CRUD operations for tasks and enforces
    business constraints like maximum task count.
    """

    def __init__(self) -> None:
        """Initialize empty task storage."""
        self._tasks: dict[int, Task] = {}

    def add(self, task: Task) -> Task:
        """
        Add a new task to the repository.

        Args:
            task: Task entity to add

        Returns:
            The added task

        Raises:
            LimitExceededError: If maximum task limit is reached
        """
        if len(self._tasks) >= settings.max_number_of_task:
            raise LimitExceededError("Task", settings.max_number_of_task)

        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: int) -> Task:
        """
        Retrieve a task by its ID.

        Args:
            task_id: Task identifier

        Returns:
            Task entity

        Raises:
            ResourceNotFoundError: If task is not found
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise ResourceNotFoundError("Task", str(task_id))
        return task

    def get_all(self) -> list[Task]:
        """
        Retrieve all tasks.

        Returns:
            List of all tasks
        """
        return list(self._tasks.values())

    def get_by_project_id(self, project_id: int) -> list[Task]:
        """
        Retrieve all tasks belonging to a specific project.

        Args:
            project_id: Project identifier

        Returns:
            List of tasks in the project
        """
        return [
            task for task in self._tasks.values() if task.project_id == project_id
        ]

    def update(self, task: Task) -> Task:
        """
        Update an existing task.

        Args:
            task: Task entity with updated data

        Returns:
            Updated task

        Raises:
            ResourceNotFoundError: If task is not found
        """
        if task.id not in self._tasks:
            raise ResourceNotFoundError("Task", str(task.id))

        self._tasks[task.id] = task
        return task

    def delete(self, task_id: int) -> None:
        """
        Delete a task by its ID.

        Args:
            task_id: Task identifier

        Raises:
            ResourceNotFoundError: If task is not found
        """
        if task_id not in self._tasks:
            raise ResourceNotFoundError("Task", str(task_id))

        del self._tasks[task_id]

    def delete_by_project_id(self, project_id: int) -> int:
        """
        Delete all tasks belonging to a specific project (cascade delete).

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks deleted
        """
        tasks_to_delete = [
            task_id
            for task_id, task in self._tasks.items()
            if task.project_id == project_id
        ]

        for task_id in tasks_to_delete:
            del self._tasks[task_id]

        return len(tasks_to_delete)

    def count(self) -> int:
        """
        Get total count of tasks.

        Returns:
            Number of tasks in repository
        """
        return len(self._tasks)

    def count_by_project_id(self, project_id: int) -> int:
        """
        Get count of tasks in a specific project.

        Args:
            project_id: Project identifier

        Returns:
            Number of tasks in the project
        """
        return sum(1 for task in self._tasks.values() if task.project_id == project_id)

    def exists(self, task_id: int) -> bool:
        """
        Check if a task exists.

        Args:
            task_id: Task identifier

        Returns:
            True if task exists, False otherwise
        """
        return task_id in self._tasks

    def clear(self) -> None:
        """Remove all tasks from repository (for testing purposes)."""
        self._tasks.clear()
