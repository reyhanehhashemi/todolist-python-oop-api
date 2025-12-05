"""
Central router registration.

This module provides a single entry point for all API routers.
"""

from fastapi import APIRouter
from .controllers import projects_controller, tasks_controller

# Create main API router
api_router = APIRouter()

# Register all controllers
api_router.include_router(
    projects_controller.router,
    prefix="/projects",
    tags=["projects"]
)

api_router.include_router(
    tasks_controller.router,
    prefix="/tasks",
    tags=["tasks"]
)

__all__ = ["api_router"]
