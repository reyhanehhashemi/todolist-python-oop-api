"""
Project service for business logic.

This module provides high-level operations for project management,
coordinating between repositories and enforcing business rules.
"""

from typing import Optional
from ..models.project import Project
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository
from ..utils.exceptions import (
    ResourceNotFoundError,
    ValidationError,
    DuplicateResourceError,
)


class ProjectService:
    """
    Service layer for project management operations.

    This class provides business logic for creating, updating,
    and managing projects, including cascade operations.
    """

    def __init__(
        self,
        project_repository: ProjectRepository,
        task_repository: TaskRepository,
    ) -> None:
        """
        Initialize project service.

        Args:
            project_repository: Repository for project persistence
            task_repository: Repository for task persistence (for cascade operations)
        """
        self._project_repo = project_repository
        self._task_repo = task_repository

    def create_project(self, title: str, description: str = "") -> Project:
        """
        Create a new project.

        Args:
            title: Project title
            description: Project description (optional)

        Returns:
            Created project

        Raises:
            ValidationError: If validation fails
            DuplicateResourceError: If project with same title exists
            LimitExceededError: If project limit is reached
        """
        # Check for duplicate title
        if self._project_repo.exists_by_title(title):
            raise DuplicateResourceError("Project", title)

        project = Project(title=title, description=description)
        return self._project_repo.add(project)

    def get_project(self, project_id: int) -> Project:
        """
        Retrieve a project by ID.

        Args:
            project_id: Project identifier

        Returns:
            Project entity

        Raises:
            ResourceNotFoundError: If project not found
        """
        return self._project_repo.get_by_id(project_id)

    def get_project_by_title(self, title: str) -> Optional[Project]:
        """
        Retrieve a project by title.

        Args:
            title: Project title

        Returns:
            Project entity if found, None otherwise
        """
        return self._project_repo.get_by_title(title)

    def get_all_projects(self) -> list[Project]:
        """
        Retrieve all projects.

        Returns:
            List of all projects
        """
        return self._project_repo.get_all()

    def update_project(
        self,
        project_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        """
        Update project details.

        Args:
            project_id: Project identifier
            title: New title (optional)
            description: New description (optional)

        Returns:
            Updated project

        Raises:
            ResourceNotFoundError: If project not found
            ValidationError: If validation fails
            DuplicateResourceError: If new title conflicts with existing project
        """
        project = self._project_repo.get_by_id(project_id)

        # Check for duplicate title if updating title
        if title is not None and title != project.title:
            existing = self._project_repo.get_by_title(title)
            if existing and existing.id != project_id:
                raise DuplicateResourceError("Project", title)

        project.update_details(title=title, description=description)
        return self._project_repo.update(project)

    def delete_project(self, project_id: int, cascade: bool = True) -> dict:
        """
        Delete a project.

        Args:
            project_id: Project identifier
            cascade: If True, also delete all tasks in the project (default: True)

        Returns:
            Dictionary with deletion statistics

        Raises:
            ResourceNotFoundError: If project not found
        """
        # Verify project exists
        self._project_repo.get_by_id(project_id)

        deleted_tasks = 0
        if cascade:
            # Cascade delete: remove all tasks in this project
            deleted_tasks = self._task_repo.delete_by_project_id(project_id)

        # Delete the project
        self._project_repo.delete(project_id)

        return {
            "project_id": project_id,
            "deleted_tasks": deleted_tasks,
            "cascade": cascade,
        }

    def count_projects(self) -> int:
        """
        Get total project count.

        Returns:
            Number of projects
        """
        return self._project_repo.count()

    def get_project_summary(self, project_id: int) -> dict:
        """
        Get summary information about a project.

        Args:
            project_id: Project identifier

        Returns:
            Dictionary with project details and task statistics

        Raises:
            ResourceNotFoundError: If project not found
        """
        project = self._project_repo.get_by_id(project_id)
        tasks = self._task_repo.get_by_project_id(project_id)

        # Count tasks by status
        from ..models.task import TaskStatus

        status_counts = {status.value: 0 for status in TaskStatus}
        for task in tasks:
            status_counts[task.status] += 1

        return {
            "project": project,
            "total_tasks": len(tasks),
            "status_breakdown": status_counts,
        }
