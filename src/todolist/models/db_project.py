"""
Database Project model using SQLAlchemy.

This module defines the Project table for PostgreSQL persistence.
"""

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from . import Base
from ..utils.exceptions import ValidationError

if TYPE_CHECKING:
    from .db_task import DBTask


class DBProject(Base):
    """
    SQLAlchemy model for Project entity.

    Attributes:
        id: Primary key (manual assignment for ID reuse)
        title: Project title (max 30 words, unique, indexed)
        description: Project description (max 150 words)
        created_at: Timestamp of creation (server default)
        updated_at: Timestamp of last update (auto-updated)
        tasks: Relationship to associated tasks
    """

    __tablename__ = "projects"

    # Primary Key - ✅ autoincrement=False برای بازیافت ID
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    # Fields
    title: Mapped[str] = mapped_column(
        String(500),  # ~30 words * 15 chars avg
        unique=True,
        nullable=False,
        index=True
    )

    description: Mapped[str] = mapped_column(
        Text,  # ~150 words
        nullable=False,
        default=""
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone= False),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    tasks: Mapped[list["DBTask"]] = relationship(
        "DBTask",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="select"
    )

    def __init__(self, id: int, title: str, description: str = "") -> None:
        """
        Initialize project with validation.

        Args:
            id: Manually assigned project ID
            title: Project title (max 30 words)
            description: Project description (max 150 words, optional)

        Raises:
            ValidationError: If validation fails
        """
        super().__init__()
        self.id = id
        self.title = title
        self.description = description

    @validates("title")
    def validate_title(self, key: str, value: str) -> str:
        """Validate title field."""
        self._validate_string_word_count(
            value,
            "Project title",
            max_words=30,
            allow_empty=False
        )
        return value

    @validates("description")
    def validate_description(self, key: str, value: str) -> str:
        """Validate description field."""
        if value:
            self._validate_string_word_count(
                value,
                "Project description",
                max_words=150,
                allow_empty=True
            )
        return value

    @staticmethod
    def _validate_string_word_count(
            value: str,
            field_name: str,
            max_words: int,
            allow_empty: bool = False
    ) -> None:
        """
        Validate string and its word count.

        Args:
            value: String value to validate
            field_name: Name of the field (for error messages)
            max_words: Maximum number of words allowed
            allow_empty: Whether empty string is allowed

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")

        if not allow_empty and (not value or not value.strip()):
            raise ValidationError(f"{field_name} cannot be empty")

        if value and value.strip():
            word_count = len(value.split())
            if word_count > max_words:
                raise ValidationError(
                    f"{field_name} must not exceed {max_words} words (current: {word_count})"
                )

    def update_details(
            self,
            title: Optional[str] = None,
            description: Optional[str] = None
    ) -> None:
        """
        Update project details.

        Args:
            title: New title (optional, max 30 words)
            description: New description (optional, max 150 words)

        Raises:
            ValidationError: If validation fails
        """
        if title is not None:
            self.title = title  # Triggers @validates

        if description is not None:
            self.description = description  # Triggers @validates

        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """Return string representation of project."""
        return f"DBProject(id={self.id}, title='{self.title}')"

    def __repr__(self) -> str:
        """Return detailed string representation of project."""
        desc_preview = (
            self.description[:50] + "..."
            if len(self.description) > 50
            else self.description
        )
        return (
            f"DBProject(id={self.id}, title='{self.title}', "
            f"description='{desc_preview}', "
            f"created_at={self.created_at.isoformat()}, "
            f"updated_at={self.updated_at.isoformat()})"
        )
