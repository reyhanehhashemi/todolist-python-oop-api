"""
Utils package initialization.

This package contains utility modules for:
- Custom exceptions
- ID generation
- Validators
- Timezone utilities
"""

from .exceptions import (
    # Base exceptions
    ToDoListException,
    ValidationError,

    # Resource not found exceptions
    ResourceNotFoundError,
    ProjectNotFoundError,
    TaskNotFoundError,

    # Duplicate exceptions
    DuplicateProjectTitleError,
    DuplicateTaskTitleError,

    # Limit exceptions
    LimitExceededError,
    MaxProjectsReachedError,
    MaxTasksReachedError,

    # Status exceptions
    InvalidTaskStatusError,
)

from .id_generator import IDGenerator
from .validators import Validators
from .timezone import get_tehran_now, to_tehran  # ✅ اضافه شد

__all__ = [
    # Exceptions
    "ToDoListException",
    "ValidationError",
    "ResourceNotFoundError",
    "ProjectNotFoundError",
    "TaskNotFoundError",
    "DuplicateProjectTitleError",
    "DuplicateTaskTitleError",
    "LimitExceededError",
    "MaxProjectsReachedError",
    "MaxTasksReachedError",
    "InvalidTaskStatusError",

    # Utils
    "IDGenerator",
    "Validators",

    # Timezone utilities  ✅ اضافه شد
    "get_tehran_now",
    "to_tehran",
]
