"""
Custom exceptions for the ToDo List application.

This module defines a hierarchy of exceptions for handling
various error conditions in the application.
"""


class ToDoListException(Exception):
    """Base exception for all ToDo List errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ValidationError(ToDoListException):
    """Raised when data validation fails."""
    pass


# ========================================
# Resource Not Found Exceptions
# ========================================

class ResourceNotFoundError(ToDoListException):
    """Base exception for resource not found errors."""

    def __init__(self, resource_type: str, resource_id: str):
        self.resource_type = resource_type
        self.resource_id = resource_id
        message = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(message)


class ProjectNotFoundError(ResourceNotFoundError):
    """Raised when a project is not found."""

    def __init__(self, project_id: str):
        super().__init__("Project", project_id)


class TaskNotFoundError(ResourceNotFoundError):
    """Raised when a task is not found."""

    def __init__(self, task_id: str):
        super().__init__("Task", task_id)


# ========================================
# Duplicate Exceptions
# ========================================

class DuplicateProjectTitleError(ToDoListException):
    """Raised when attempting to create a project with a duplicate title."""

    def __init__(self, title: str):
        message = f"Project with title '{title}' already exists"
        super().__init__(message)


class DuplicateTaskTitleError(ToDoListException):
    """Raised when attempting to create a task with a duplicate title in the same project."""

    def __init__(self, title: str, project_id: int):
        message = f"Task with title '{title}' already exists in project {project_id}"
        super().__init__(message)


# ========================================
# Duplicate Exceptions
# ========================================

class DuplicateResourceError(ToDoListException):
    """Base exception for duplicate resource errors."""

    def __init__(self, resource_type: str, identifier: str):
        self.resource_type = resource_type
        self.identifier = identifier
        message = f"{resource_type} with identifier '{identifier}' already exists"
        super().__init__(message)


class DuplicateProjectTitleError(DuplicateResourceError):
    """Raised when attempting to create a project with a duplicate title."""

    def __init__(self, title: str):
        super().__init__("Project", title)


class DuplicateTaskTitleError(DuplicateResourceError):
    """Raised when attempting to create a task with a duplicate title in the same project."""

    def __init__(self, title: str, project_id: int):
        message = f"Task with title '{title}' already exists in project {project_id}"
        # Override parent message
        ToDoListException.__init__(self, message)
        self.resource_type = "Task"
        self.identifier = title


# ========================================
# Limit Exceeded Exceptions
# ========================================

class LimitExceededError(ToDoListException):
    """Base exception for limit exceeded errors."""

    def __init__(self, resource_type: str, limit: int):
        self.resource_type = resource_type
        self.limit = limit
        message = f"Maximum {resource_type.lower()} limit of {limit} has been reached"
        super().__init__(message)


class MaxProjectsReachedError(LimitExceededError):
    """Raised when maximum number of projects is reached."""

    def __init__(self, limit: int):
        super().__init__("Project", limit)


class MaxTasksReachedError(LimitExceededError):
    """Raised when maximum number of tasks is reached."""

    def __init__(self, limit: int):
        super().__init__("Task", limit)


# ========================================
# Status Exceptions
# ========================================

class InvalidTaskStatusError(ToDoListException):
    """Raised when an invalid task status is provided."""

    def __init__(self, status: str, valid_statuses: list[str]):
        message = (
            f"Invalid status '{status}'. "
            f"Valid statuses are: {', '.join(valid_statuses)}"
        )
        super().__init__(message)
