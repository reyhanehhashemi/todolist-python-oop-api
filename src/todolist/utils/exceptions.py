"""
Custom exceptions for the ToDo List application.

This module defines domain-specific exceptions to provide clear
error handling and meaningful error messages.
"""


class ToDoListException(Exception):
    """Base exception for all ToDo List application errors."""

    pass


class ValidationError(ToDoListException):
    """Raised when validation of input data fails."""

    pass


class ResourceNotFoundError(ToDoListException):
    """Raised when a requested resource (project/task) is not found."""

    def __init__(self, resource_type: str, identifier: str) -> None:
        """
        Initialize ResourceNotFoundError.

        Args:
            resource_type: Type of resource (e.g., "Project", "Task")
            identifier: Identifier of the resource (e.g., ID, title)
        """
        self.resource_type = resource_type
        self.identifier = identifier
        super().__init__(
            f"{resource_type} with identifier '{identifier}' not found"
        )


class LimitExceededError(ToDoListException):
    """Raised when attempting to exceed maximum allowed items."""

    def __init__(self, resource_type: str, limit: int) -> None:
        """
        Initialize LimitExceededError.

        Args:
            resource_type: Type of resource (e.g., "Project", "Task")
            limit: Maximum allowed count
        """
        self.resource_type = resource_type
        self.limit = limit
        super().__init__(
            f"Cannot create more {resource_type}s. "
            f"Maximum limit of {limit} reached"
        )


class DuplicateResourceError(ToDoListException):
    """Raised when attempting to create a resource that already exists."""

    def __init__(self, resource_type: str, identifier: str) -> None:
        """
        Initialize DuplicateResourceError.

        Args:
            resource_type: Type of resource (e.g., "Project", "Task")
            identifier: Identifier of the duplicate resource
        """
        self.resource_type = resource_type
        self.identifier = identifier
        super().__init__(
            f"{resource_type} with identifier '{identifier}' already exists"
        )


class InvalidStatusError(ToDoListException):
    """Raised when an invalid status value is provided."""

    def __init__(self, provided_status: str, valid_statuses: list[str]) -> None:
        """
        Initialize InvalidStatusError.

        Args:
            provided_status: The invalid status value provided
            valid_statuses: List of valid status values
        """
        self.provided_status = provided_status
        self.valid_statuses = valid_statuses
        super().__init__(
            f"Invalid status '{provided_status}'. "
            f"Valid statuses are: {', '.join(valid_statuses)}"
        )
"""
Custom exceptions for the todolist application.
"""


class TodoListException(Exception):
    """Base exception for todolist application."""
    pass


class ValidationError(TodoListException):
    """Raised when validation fails."""
    pass


class ProjectNotFoundError(TodoListException):
    """Raised when a project is not found."""
    pass


class MaxProjectsReachedError(TodoListException):
    """Raised when maximum number of projects is reached."""
    pass


class TaskNotFoundError(TodoListException):
    """Raised when a task is not found."""
    pass


class MaxTasksReachedError(TodoListException):
    """Raised when maximum number of tasks is reached."""
    pass
