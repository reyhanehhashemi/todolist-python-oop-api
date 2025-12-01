"""
Project domain model.

This module defines the Project entity representing a collection
of related tasks.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


def _generate_project_id() -> int:
    """Generate unique ID for project."""
    try:
        from ..utils.id_generator import id_generator
        return id_generator.generate('project')
    except (ImportError, AttributeError):
        return int(datetime.now().timestamp() * 1000000)


@dataclass
class Project:
    """
    Project entity representing a collection of related tasks.

    Attributes:
        id: Unique identifier (integer)
        title: Project title (max 30 words)
        description: Detailed description of the project (max 150 words)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """

    title: str
    description: str = ""
    id: int = field(default_factory=_generate_project_id)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate project data after initialization."""
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

    def _validate(self) -> None:
        """
        Validate project attributes.

        Raises:
            ValidationError: If validation fails
        """
        # Validate title (required, max 30 words)
        self._validate_string_word_count(
            self.title,
            "Project title",
            max_words=30,
            allow_empty=False
        )

        # Validate description (optional, max 150 words)
        if self.description:
            self._validate_string_word_count(
                self.description,
                "Project description",
                max_words=150,
                allow_empty=True
            )

    def update_details(
            self, title: Optional[str] = None, description: Optional[str] = None
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
            self._validate_string_word_count(
                title,
                "Project title",
                max_words=30,
                allow_empty=False
            )
            self.title = title

        if description is not None:
            self._validate_string_word_count(
                description,
                "Project description",
                max_words=150,
                allow_empty=True
            )
            self.description = description

        self.updated_at = datetime.now()

    def __str__(self) -> str:
        """Return string representation of project."""
        return f"Project(id={self.id}, title='{self.title}')"

    def __repr__(self) -> str:
        """Return detailed string representation of project."""
        desc_preview = self.description[:50] + "..." if len(self.description) > 50 else self.description
        return (
            f"Project(id={self.id}, title='{self.title}', "
            f"description='{desc_preview}', "
            f"created_at={self.created_at.isoformat()}, "
            f"updated_at={self.updated_at.isoformat()})"
        )
