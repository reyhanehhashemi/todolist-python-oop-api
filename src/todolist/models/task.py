"""
Task domain model.

This module defines the Task entity representing a single task
within a project.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


def _generate_task_id() -> int:
    """Generate unique ID for task."""
    try:
        from ..utils.id_generator import id_generator
        return id_generator.generate('task')
    except (ImportError, AttributeError):
        return int(datetime.now().timestamp() * 1000000)


class TaskStatus(str, Enum):
    """Enumeration of valid task statuses."""

    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"

    @classmethod
    def values(cls) -> list[str]:
        """Return list of all valid status values."""
        return [status.value for status in cls]


@dataclass
class Task:
    """
    Task entity representing a single task within a project.

    Attributes:
        id: Unique identifier (integer)
        title: Task title (max 30 words)
        description: Detailed description of the task (max 150 words)
        status: Current status (TODO, DOING, DONE)
        project_id: ID of the parent project
        deadline: Optional deadline for the task
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """

    title: str
    project_id: int
    description: str = ""
    status: str = TaskStatus.TODO.value
    deadline: Optional[datetime] = None
    id: int = field(default_factory=_generate_task_id)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate task data after initialization."""
        self._validate()

    def _validate_string_word_count(
        self,
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
        from ..utils.exceptions import ValidationError

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

    def _validate_status(self, status_value: str, field_name: str) -> None:
        """
        Validate task status.

        Args:
            status_value: Status value to validate
            field_name: Name of the field (for error messages)

        Raises:
            ValidationError: If status is invalid
        """
        from ..utils.exceptions import ValidationError

        valid_statuses = TaskStatus.values()
        if status_value not in valid_statuses:
            raise ValidationError(
                f"{field_name} must be one of {valid_statuses}, got '{status_value}'"
            )

    def _validate(self) -> None:
        """
        Validate task attributes.

        Raises:
            ValidationError: If validation fails
        """
        from ..utils.exceptions import ValidationError

        # Validate title (required, max 30 words)
        self._validate_string_word_count(
            self.title,
            "Task title",
            max_words=30,
            allow_empty=False
        )

        # Validate project_id is an integer
        if not isinstance(self.project_id, int):
            raise ValidationError("Project ID must be an integer")

        # Validate status
        self._validate_status(self.status, "Task status")

        # Validate description (optional, max 150 words)
        if self.description:
            self._validate_string_word_count(
                self.description,
                "Task description",
                max_words=150,
                allow_empty=True
            )

        # Validate deadline if provided
        self._validate_deadline()

    def _validate_deadline(self) -> None:
        """
        Validate deadline is in the future.

        Raises:
            ValidationError: If deadline is in the past
        """
        from ..utils.exceptions import ValidationError

        if self.deadline is None:
            return

        if not isinstance(self.deadline, datetime):
            raise ValidationError("Task deadline must be a datetime object")

        # Remove microseconds for fair comparison
        now = datetime.now().replace(microsecond=0)
        deadline_normalized = self.deadline.replace(microsecond=0)

        if deadline_normalized < now:
            raise ValidationError("Task deadline cannot be in the past")

    def update_status(self, new_status: str) -> None:
        """
        Update task status.

        Args:
            new_status: New status value

        Raises:
            ValidationError: If status is invalid
        """
        self._validate_status(new_status, "New status")
        self.status = new_status
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
            self._validate_string_word_count(
                title,
                "Task title",
                max_words=30,
                allow_empty=False
            )
            self.title = title

        if description is not None:
            self._validate_string_word_count(
                description,
                "Task description",
                max_words=150,
                allow_empty=True
            )
            self.description = description

        # Update deadline if provided (even if it's the same value)
        # This allows the validation to run again
        if deadline is not None:
            self.deadline = deadline
            self._validate_deadline()

        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """Return string representation of task."""
        deadline_str = f", deadline={self.deadline.strftime('%Y-%m-%d %H:%M')}" if self.deadline else ""
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"status={self.status}{deadline_str})"
        )

    def __repr__(self) -> str:
        """Return detailed string representation of task."""
        deadline_str = self.deadline.isoformat() if self.deadline else "None"
        desc_preview = self.description[:50] + "..." if len(self.description) > 50 else self.description
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"description='{desc_preview}', "
            f"status='{self.status}', project_id={self.project_id}, "
            f"deadline={deadline_str}, "
            f"created_at={self.created_at.isoformat()}, "
            f"updated_at={self.updated_at.isoformat()})"
        )
