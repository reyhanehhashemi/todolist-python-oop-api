"""
API Package.

This package contains the FastAPI application components:
- Routers: HTTP endpoint handlers
- Schemas: Pydantic models for validation
- Dependencies: Dependency injection utilities
"""

from .dependencies import (
    get_db,
    get_project_service,
    get_task_service,
    DatabaseSession,
    ProjectService,
    TaskService,
)

__all__ = [
    "get_db",
    "get_project_service",
    "get_task_service",
    "DatabaseSession",
    "ProjectService",
    "TaskService",
]
