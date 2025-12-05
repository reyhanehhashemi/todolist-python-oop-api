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
from ..utils import get_tehran_now  # ✅ اضافه شد

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

    All datetime fields are stored as naive (timezone=False) in Tehran time.
    """

    __tablename__ = "tasks"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)

    # Fields
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True
    )

    description: Mapped[str] = mapped_column(
        Text,
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

    # ✅ تغییر به timezone=False (naive)
    deadline: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False),  # ✅ naive
        nullable=True
    )

    closed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=False),  # ✅ naive
        nullable=True
    )

    # Timestamps (naive, Tehran time)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),  # ✅ naive
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),  # ✅ naive
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
        """Initialize task with validation."""
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
        """Validate deadline field (must be in future, Tehran time)."""
        if value is None:
            return value

        if not isinstance(value, datetime):
            raise ValidationError("Task deadline must be a datetime object")

        # ✅ مقایسه با وقت تهران (naive)
        now = get_tehran_now().replace(microsecond=0)
        deadline_normalized = value.replace(microsecond=0)

        if deadline_normalized < now:
            raise ValidationError(
                f"Task deadline cannot be in the past. "
                f"Current time (Tehran): {now.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        return value

    @staticmethod
    def _validate_string_word_count(
            value: str,
            field_name: str,
            max_words: int,
            allow_empty: bool = False
    ) -> None:
        """Validate string and its word count."""
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
        """Update task status."""
        self.status = new_status
        self.updated_at = get_tehran_now()  # ✅ Tehran naive

    def update_details(
            self,
            title: Optional[str] = None,
            description: Optional[str] = None,
            deadline: Optional[datetime] = None
    ) -> None:
        """Update task details."""
        if title is not None:
            self.title = title

        if description is not None:
            self.description = description

        if deadline is not None:
            self.deadline = deadline

        self.updated_at = get_tehran_now()  # ✅ Tehran naive

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
