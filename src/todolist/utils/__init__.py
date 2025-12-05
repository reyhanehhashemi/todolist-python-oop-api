"""
Utils package initialization.

This package contains utility modules for:
- Custom exceptions
- ID generation
- Validators
"""

from .exceptions import (
    # Base exceptions
    ToDoListException,
    ValidationError,

    # Resource not found exceptions
    ResourceNotFoundError,  # ✅ اضافه شد
    ProjectNotFoundError,
    TaskNotFoundError,

    # Duplicate exceptions
    DuplicateProjectTitleError,
    DuplicateTaskTitleError,

    # Limit exceptions
    LimitExceededError,  # ✅ اضافه شد
    MaxProjectsReachedError,
    MaxTasksReachedError,

    # Status exceptions
    InvalidTaskStatusError,
)

from .id_generator import IDGenerator
from .validators import Validators

__all__ = [
    # Exceptions
    "ToDoListException",
    "ValidationError",
    "ResourceNotFoundError",  # ✅ اضافه شد
    "ProjectNotFoundError",
    "TaskNotFoundError",
    "DuplicateProjectTitleError",
    "DuplicateTaskTitleError",
    "LimitExceededError",  # ✅ اضافه شد
    "MaxProjectsReachedError",
    "MaxTasksReachedError",
    "InvalidTaskStatusError",

    # Utils
    "IDGenerator",
    "Validators",
]
