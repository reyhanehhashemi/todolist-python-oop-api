"""
API Schema exports.

This module provides a central point for importing all Pydantic schemas
used in the API layer.
"""

from .task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskResponse,
    TaskStatusEnum
)

from .project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    ProjectList,
    TaskStatistics
)

from .common import ErrorResponse  # اضافه شد

__all__ = [
    # Task schemas
    'TaskCreate',
    'TaskUpdate',
    'TaskStatusUpdate',
    'TaskResponse',
    'TaskStatusEnum',

    # Project schemas
    'ProjectCreate',
    'ProjectUpdate',
    'ProjectResponse',
    'ProjectDetailResponse',
    'ProjectList',
    'TaskStatistics',

    # Common schemas
    'ErrorResponse'  # اضافه شد
]
