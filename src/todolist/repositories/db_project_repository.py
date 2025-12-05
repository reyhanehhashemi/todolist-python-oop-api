"""
Database-backed project repository for data persistence.

This module provides PostgreSQL storage and retrieval operations
for Project entities using SQLAlchemy ORM.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.db_project import DBProject
from ..utils.exceptions import ResourceNotFoundError, LimitExceededError
from ..utils import get_tehran_now  # ✅ اضافه شد
from ..config import settings


class DBProjectRepository:
    """
    Repository for managing Project entities in PostgreSQL.

    This class provides CRUD operations for projects and enforces
    business constraints like maximum project count.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize project repository with database session.

        Args:
            session: SQLAlchemy database session
        """
        self._session = session

    def _get_next_id(self) -> int:
        """
        Get the next available project ID by finding the first gap.

        Returns:
            Next available ID (smallest unused positive integer)
        """
        # Get all existing IDs sorted
        existing_ids = [
            row[0] for row in self._session.query(DBProject.id).order_by(DBProject.id).all()
        ]

        # Find first gap
        next_id = 1
        for existing_id in existing_ids:
            if existing_id == next_id:
                next_id += 1
            elif existing_id > next_id:
                break

        return next_id

    def add(self, title: str, description: str = "") -> DBProject:
        """
        Add a new project to the database.

        Args:
            title: Project title
            description: Project description (optional)

        Returns:
            The created project

        Raises:
            LimitExceededError: If maximum project limit is reached
        """
        # Check project limit
        if self.count() >= settings.max_number_of_project:
            raise LimitExceededError("Project", settings.max_number_of_project)

        # Get next available ID
        next_id = self._get_next_id()

        # Create new project with manual ID and Tehran time
        project = DBProject(
            id=next_id,
            title=title,
            description=description,

        )

        self._session.add(project)
        self._session.flush()  # Flush to get the ID assigned
        return project

    def get_by_id(self, project_id: int) -> DBProject:
        """
        Retrieve a project by its ID.

        Args:
            project_id: Project identifier

        Returns:
            Project entity

        Raises:
            ResourceNotFoundError: If project is not found
        """
        project = self._session.query(DBProject).filter(DBProject.id == project_id).first()
        if project is None:
            raise ResourceNotFoundError("Project", str(project_id))
        return project

    def get_by_title(self, title: str) -> Optional[DBProject]:
        """
        Retrieve a project by its title (case-insensitive).

        Args:
            title: Project title

        Returns:
            Project entity if found, None otherwise
        """
        return (
            self._session.query(DBProject)
            .filter(func.lower(DBProject.title) == title.lower())
            .first()
        )

    def get_all(self) -> list[DBProject]:
        """
        Retrieve all projects.

        Returns:
            List of all projects
        """
        return self._session.query(DBProject).order_by(DBProject.id).all()

    def update(self, project: DBProject) -> DBProject:
        """
        Update an existing project.

        Args:
            project: Project entity with updated data

        Returns:
            Updated project

        Raises:
            ResourceNotFoundError: If project is not found
        """
        existing = self._session.query(DBProject).filter(DBProject.id == project.id).first()
        if existing is None:
            raise ResourceNotFoundError("Project", str(project.id))

        self._session.merge(project)
        self._session.flush()
        return project

    def delete(self, project_id: int) -> None:
        """
        Delete a project by its ID.

        Args:
            project_id: Project identifier

        Raises:
            ResourceNotFoundError: If project is not found
        """
        project = self.get_by_id(project_id)
        self._session.delete(project)
        self._session.flush()

    def count(self) -> int:
        """
        Get total count of projects.

        Returns:
            Number of projects in database
        """
        return self._session.query(DBProject).count()

    def exists(self, project_id: int) -> bool:
        """
        Check if a project exists.

        Args:
            project_id: Project identifier

        Returns:
            True if project exists, False otherwise
        """
        return (
            self._session.query(DBProject)
            .filter(DBProject.id == project_id)
            .count()
            > 0
        )

    def exists_by_title(self, title: str) -> bool:
        """
        Check if a project with given title exists (case-insensitive).

        Args:
            title: Project title

        Returns:
            True if project exists, False otherwise
        """
        return self.get_by_title(title) is not None

    def clear(self) -> None:
        """Remove all projects from database (for testing purposes)."""
        self._session.query(DBProject).delete()
        self._session.flush()
