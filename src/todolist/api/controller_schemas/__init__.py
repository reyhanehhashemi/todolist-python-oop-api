"""
Controller Schemas Package.

Contains all Pydantic models for API request/response validation.
"""

from .requests import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskStatusUpdateRequest
)

from .responses import (
    ProjectResponse,
    ProjectDetailResponse,
    TaskStatistics,
    TaskResponse
)

from .common import ErrorResponse

__all__ = [
    # Requests
    "ProjectCreateRequest",
    "ProjectUpdateRequest",
    "TaskCreateRequest",
    "TaskUpdateRequest",
    "TaskStatusUpdateRequest",

    # Responses
    "ProjectResponse",
    "ProjectDetailResponse",
    "TaskStatistics",
    "TaskResponse",

    # Common
    "ErrorResponse",
]
