"""
Database Task model using SQLAlchemy.

This module defines the Task table for PostgreSQL persistence.
"""

from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, Text, DateTime, Integer, ForeignKey, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from . import Base
from ..utils.exceptions import ValidationError

if TYPE_CHECKING:
    from .db_project import DBProject


class TaskStatus(str, PyEnum):
    """Enumeration of valid task statuses."""

    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"

    @classmethod
    def values(cls) -> list[str]:
        """Return list of all valid status values."""
        return [status.value for status in cls]


class DBTask(Base):
    """
    SQLAlchemy model for Task entity.

    Attributes:
        id: Primary key (manual assignment for ID reuse)
        title: Task title (max 30 words, indexed)
        description: Task description (max 150 words)
        status: Current status (TODO, DOING, DONE)
        project_id: Foreign key to projects table
        deadline: Optional deadline for the task
        created_at: Timestamp of creation (server default)
        updated_at: Timestamp of last update (auto-updated)
        project: Relationship to parent project
    """

    __tablename__ = "tasks"

    # Primary Key - ✅ autoincrement=False برای بازیافت ID
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    # Fields
    title: Mapped[str] = mapped_column(
        String(500),  # ~30 words * 15 chars avg
        nullable=False,
        index=True
    )

    description: Mapped[str] = mapped_column(
        Text,  # ~150 words
        nullable=False,
        default=""
    )

    status: Mapped[str] = mapped_column(
        Enum(TaskStatus, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=TaskStatus.TODO.value,
        index=True
    )

    # Foreign Key
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Optional deadline
    deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    closed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
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
    project: Mapped["DBProject"] = relationship(
        "DBProject",
        back_populates="tasks"
    )

    def __init__(
            self,
            id: int,
            title: str,
            project_id: int,
            description: str = "",
            status: str = TaskStatus.TODO.value,
            deadline: Optional[datetime] = None
    ) -> None:
        """
        Initialize task with validation.

        Args:
            id: Manually assigned task ID
            title: Task title (max 30 words)
            project_id: ID of the parent project
            description: Task description (max 150 words, optional)
            status: Task status (default: TODO)
            deadline: Optional deadline for the task

        Raises:
            ValidationError: If validation fails
        """
        super().__init__()
        self.id = id
        self.title = title
        self.project_id = project_id
        self.description = description
        self.status = status
        self.deadline = deadline

    @validates("title")
    def validate_title(self, key: str, value: str) -> str:
        """Validate title field."""
        self._validate_string_word_count(
            value,
            "Task title",
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
                "Task description",
                max_words=150,
                allow_empty=True
            )
        return value

    @validates("status")
    def validate_status_field(self, key: str, value: str) -> str:
        """Validate status field."""
        valid_statuses = TaskStatus.values()
        if value not in valid_statuses:
            raise ValidationError(
                f"Task status must be one of {valid_statuses}, got '{value}'"
            )
        return value

    @validates("deadline")
    def validate_deadline_field(self, key: str, value: Optional[datetime]) -> Optional[datetime]:
        """Validate deadline field."""
        if value is None:
            return value

        if not isinstance(value, datetime):
            raise ValidationError("Task deadline must be a datetime object")

        # Remove microseconds for fair comparison
        now = datetime.now().replace(microsecond=0)
        deadline_normalized = value.replace(microsecond=0)

        if deadline_normalized < now:
            raise ValidationError("Task deadline cannot be in the past")

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

    def update_status(self, new_status: str) -> None:
        """
        Update task status.

        Args:
            new_status: New status value

        Raises:
            ValidationError: If status is invalid
        """
        self.status = new_status  # Triggers @validates
        self.updated_at = datetime.now()

    def update_details(
            self,
            title: Optional[str] = None,
            description: Optional[str] = None,
            deadline: Optional[datetime] = None
    ) -> None:
        """
        Update task details.

        Args:
            title: New title (optional, max 30 words)
            description: New description (optional, max 150 words)
            deadline: New deadline (optional)

        Raises:
            ValidationError: If validation fails
        """
        if title is not None:
            self.title = title  # Triggers @validates

        if description is not None:
            self.description = description  # Triggers @validates

        if deadline is not None:
            self.deadline = deadline  # Triggers @validates

        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """Return string representation of task."""
        deadline_str = (
            f", deadline={self.deadline.strftime('%Y-%m-%d %H:%M')}"
            if self.deadline
            else ""
        )
        return (
            f"DBTask(id={self.id}, title='{self.title}', "
            f"status={self.status}{deadline_str})"
        )

    def __repr__(self) -> str:
        """Return detailed string representation of task."""
        deadline_str = self.deadline.isoformat() if self.deadline else "None"
        desc_preview = (
            self.description[:50] + "..."
            if len(self.description) > 50
            else self.description
        )
        return (
            f"DBTask(id={self.id}, title='{self.title}', "
            f"description='{desc_preview}', "
            f"status='{self.status}', project_id={self.project_id}, "
            f"deadline={deadline_str}, "
            f"created_at={self.created_at.isoformat()}, "
            f"updated_at={self.updated_at.isoformat()})"
        )
