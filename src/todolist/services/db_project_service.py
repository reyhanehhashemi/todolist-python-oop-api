"""
Database-backed project service for business logic.

This module provides high-level operations for project management
using PostgreSQL database.
"""

from typing import Optional
from sqlalchemy.orm import Session
from ..models.db_project import DBProject
from ..repositories.db_project_repository import DBProjectRepository
from ..repositories.db_task_repository import DBTaskRepository
from ..utils.exceptions import (
    ResourceNotFoundError,
    DuplicateResourceError,
)


class DBProjectService:
    """
    Service layer for project management operations (Database-backed).

    This class provides business logic for creating, updating,
    and managing projects with PostgreSQL persistence.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize project service with database session.

        Args:
            session: SQLAlchemy database session
        """
        self._session = session
        self._project_repo = DBProjectRepository(session)
        self._task_repo = DBTaskRepository(session)

    def create_project(self, title: str, description: str = "") -> DBProject:
        """
        Create a new project.

        Args:
            title: Project title
            description: Project description (optional)

        Returns:
            Created project

        Raises:
            DuplicateResourceError: If project with same title exists
        """
        # Check for duplicate title
        if self._project_repo.exists_by_title(title):
            raise DuplicateResourceError("Project", title)

        # ✅ Repository خودش object میسازه
        created_project = self._project_repo.add(title=title, description=description)
        self._session.commit()
        return created_project

    def get_project(self, project_id: int) -> DBProject:
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

    def get_project_by_title(self, title: str) -> Optional[DBProject]:
        """
        Retrieve a project by title.

        Args:
            title: Project title

        Returns:
            Project entity if found, None otherwise
        """
        return self._project_repo.get_by_title(title)

    def get_all_projects(self) -> list[DBProject]:
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
    ) -> DBProject:
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
            DuplicateResourceError: If new title conflicts with existing project
        """
        project = self._project_repo.get_by_id(project_id)

        # Check for duplicate title if updating title
        if title is not None and title != project.title:
            existing = self._project_repo.get_by_title(title)
            if existing and existing.id != project_id:
                raise DuplicateResourceError("Project", title)

        # Update fields
        if title is not None:
            project.title = title
        if description is not None:
            project.description = description

        updated_project = self._project_repo.update(project)
        self._session.commit()
        return updated_project

    def delete_project(self, project_id: int, cascade: bool = True) -> dict:
        """
        Delete a project.

        Args:
            project_id: Project identifier
            cascade: If True, database CASCADE will handle task deletion

        Returns:
            Dictionary with deletion statistics

        Raises:
            ResourceNotFoundError: If project not found
        """
        # Verify project exists
        project = self._project_repo.get_by_id(project_id)

        # Count tasks before deletion (for statistics)
        tasks = self._task_repo.get_by_project_id(project_id)
        deleted_tasks = len(tasks)

        # Delete the project (CASCADE will handle tasks automatically)
        self._project_repo.delete(project_id)
        self._session.commit()

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
        project = self.get_project(project_id)

        # Get all tasks for this project
        tasks = self._task_repo.get_by_project_id(project_id)

        # Count tasks by status
        from ..models.db_task import TaskStatus

        status_counts = {status.value: 0 for status in TaskStatus}
        for task in tasks:
            status_counts[task.status.value] += 1

        return {
            "project": project,
            "total_tasks": len(tasks),
            "status_breakdown": status_counts,
        }

    def commit(self) -> None:
        """Commit current transaction."""
        self._session.commit()

    def rollback(self) -> None:
        """Rollback current transaction."""
        self._session.rollback()
