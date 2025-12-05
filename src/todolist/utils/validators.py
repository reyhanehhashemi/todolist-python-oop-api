"""
Validation utilities for the ToDo List application.

This module provides validation functions to ensure data integrity
and enforce business rules.
"""

from typing import Optional
from .exceptions import ValidationError


class Validators:
    """Static validation utilities for the ToDo List application."""

    @staticmethod
    def validate_non_empty_string(
        value: str, field_name: str, max_length: Optional[int] = None
    ) -> None:
        """
        Validate that a string is non-empty and within length constraints.

        Args:
            value: String value to validate
            field_name: Name of the field (for error messages)
            max_length: Maximum allowed length (optional)

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, str):
            raise ValidationError(f"{field_name} must be a string")

        if not value or not value.strip():
            raise ValidationError(f"{field_name} cannot be empty")

        if max_length and len(value) > max_length:
            raise ValidationError(
                f"{field_name} cannot exceed {max_length} characters. "
                f"Got {len(value)} characters"
            )

    @staticmethod
    def validate_positive_integer(value: int, field_name: str) -> None:
        """
        Validate that a value is a positive integer.

        Args:
            value: Integer value to validate
            field_name: Name of the field (for error messages)

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(value, int):
            raise ValidationError(f"{field_name} must be an integer")

        if value < 0:
            raise ValidationError(f"{field_name} must be non-negative")

    @staticmethod
    def validate_status(
        status: str, valid_statuses: list[str], field_name: str = "Status"
    ) -> None:
        """
        Validate that a status value is within allowed values.

        Args:
            status: Status value to validate
            valid_statuses: List of valid status values
            field_name: Name of the field (for error messages)

        Raises:
            ValidationError: If validation fails
        """
        if not isinstance(status, str):
            raise ValidationError(f"{field_name} must be a string")

        if status not in valid_statuses:
            raise ValidationError(
                f"{field_name} must be one of: {', '.join(valid_statuses)}. "
                f"Got '{status}'"
            )


# Export validator functions at module level for convenience
validate_non_empty_string = Validators.validate_non_empty_string
validate_positive_integer = Validators.validate_positive_integer
validate_status = Validators.validate_status
