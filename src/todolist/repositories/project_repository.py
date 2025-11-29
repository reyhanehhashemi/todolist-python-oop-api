"""
Project repository for data persistence.

This module provides in-memory storage and retrieval operations
for Project entities.
"""

from typing import Optional
from ..models.project import Project
from ..utils.exceptions import ResourceNotFoundError, LimitExceededError
from ..config import settings


class ProjectRepository:
    """
    Repository for managing Project entities in memory.

    This class provides CRUD operations for projects and enforces
    business constraints like maximum project count.
    """

    def __init__(self) -> None:
        """Initialize empty project storage."""
        self._projects: dict[int, Project] = {}

    def add(self, project: Project) -> Project:
        """
        Add a new project to the repository.

        Args:
            project: Project entity to add

        Returns:
            The added project

        Raises:
            LimitExceededError: If maximum project limit is reached
        """
        if len(self._projects) >= settings.max_number_of_project:
            raise LimitExceededError("Project", settings.max_number_of_project)

        self._projects[project.id] = project
        return project

    def get_by_id(self, project_id: int) -> Project:
        """
        Retrieve a project by its ID.

        Args:
            project_id: Project identifier

        Returns:
            Project entity

        Raises:
            ResourceNotFoundError: If project is not found
        """
        project = self._projects.get(project_id)
        if project is None:
            raise ResourceNotFoundError("Project", str(project_id))
        return project

    def get_by_title(self, title: str) -> Optional[Project]:
        """
        Retrieve a project by its title.

        Args:
            title: Project title

        Returns:
            Project entity if found, None otherwise
        """
        for project in self._projects.values():
            if project.title.lower() == title.lower():
                return project
        return None

    def get_all(self) -> list[Project]:
        """
        Retrieve all projects.

        Returns:
            List of all projects
        """
        return list(self._projects.values())

    def update(self, project: Project) -> Project:
        """
        Update an existing project.

        Args:
            project: Project entity with updated data

        Returns:
            Updated project

        Raises:
            ResourceNotFoundError: If project is not found
        """
        if project.id not in self._projects:
            raise ResourceNotFoundError("Project", str(project.id))

        self._projects[project.id] = project
        return project

    def delete(self, project_id: int) -> None:
        """
        Delete a project by its ID.

        Args:
            project_id: Project identifier

        Raises:
            ResourceNotFoundError: If project is not found
        """
        if project_id not in self._projects:
            raise ResourceNotFoundError("Project", str(project_id))

        del self._projects[project_id]

    def count(self) -> int:
        """
        Get total count of projects.

        Returns:
            Number of projects in repository
        """
        return len(self._projects)

    def exists(self, project_id: int) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: Project identifier

        Returns:
            True if project exists, False otherwise
        """
        return project_id in self._projects

    def exists_by_title(self, title: str) -> bool:
        """
        Check if a project with given title exists.

        Args:
            title: Project title

        Returns:
            True if project exists, False otherwise
        """
        return self.get_by_title(title) is not None

    def clear(self) -> None:
        """Remove all projects from repository (for testing purposes)."""
        self._projects.clear()
