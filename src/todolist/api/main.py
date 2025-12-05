"""
FastAPI application entry point.

This module sets up the FastAPI application with:
- Router registration
- Exception handlers
- Middleware configuration
- Database initialization
- API documentation
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# ✅ Import از db package (نه models)
from todolist.db.database import engine
from todolist.models.db_base import Base

# ✅ Import routers
from todolist.api.routers.projects import router as projects_router
from todolist.api.routers.tasks import router as tasks_router

# ✅ Import exceptions از exceptions.py
from todolist.utils.exceptions import (
    ToDoListException,
    ValidationError,
    ProjectNotFoundError,
    TaskNotFoundError,
    DuplicateProjectTitleError,
    DuplicateTaskTitleError,
    MaxProjectsReachedError,
    MaxTasksReachedError,
    InvalidTaskStatusError,
)


# ============================================================================
# LIFESPAN EVENTS
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan manager.

    Handles startup and shutdown events:
    - Startup: Create database tables
    - Shutdown: Cleanup resources
    """
    # Startup: Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")

    yield

    # Shutdown: Cleanup (if needed)
    print("🔽 Application shutting down...")


# ============================================================================
# APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="ToDo List API",
    description="A RESTful API for managing projects and tasks",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ============================================================================
# MIDDLEWARE
# ============================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در production محدود کنید
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(ValidationError)
async def validation_error_handler(
    request: Request,
    exc: ValidationError
) -> JSONResponse:
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": str(exc),
            "type": "validation_error"
        }
    )


@app.exception_handler(ProjectNotFoundError)
async def project_not_found_handler(
    request: Request,
    exc: ProjectNotFoundError
) -> JSONResponse:
    """Handle project not found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
            "type": "project_not_found",
            "project_id": exc.project_id
        }
    )


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundError
) -> JSONResponse:
    """Handle task not found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
            "type": "task_not_found",
            "task_id": exc.task_id
        }
    )


@app.exception_handler(DuplicateProjectTitleError)
async def duplicate_project_handler(
    request: Request,
    exc: DuplicateProjectTitleError
) -> JSONResponse:
    """Handle duplicate project title errors."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
            "type": "duplicate_project",
            "title": exc.title
        }
    )


@app.exception_handler(DuplicateTaskTitleError)
async def duplicate_task_handler(
    request: Request,
    exc: DuplicateTaskTitleError
) -> JSONResponse:
    """Handle duplicate task title errors."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
            "type": "duplicate_task",
            "title": exc.title,
            "project_id": exc.project_id
        }
    )


@app.exception_handler(MaxProjectsReachedError)
async def max_projects_handler(
    request: Request,
    exc: MaxProjectsReachedError
) -> JSONResponse:
    """Handle max projects limit errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "type": "max_projects_reached",
            "limit": exc.limit
        }
    )


@app.exception_handler(MaxTasksReachedError)
async def max_tasks_handler(
    request: Request,
    exc: MaxTasksReachedError
) -> JSONResponse:
    """Handle max tasks limit errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "type": "max_tasks_reached",
            "limit": exc.limit
        }
    )


@app.exception_handler(InvalidTaskStatusError)
async def invalid_status_handler(
    request: Request,
    exc: InvalidTaskStatusError
) -> JSONResponse:
    """Handle invalid task status errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "type": "invalid_status",
            "provided_status": exc.provided_status,
            "valid_statuses": exc.valid_statuses
        }
    )


@app.exception_handler(ToDoListException)
async def todolist_exception_handler(
    request: Request,
    exc: ToDoListException
) -> JSONResponse:
    """Handle all other ToDoList exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": str(exc),
            "type": "todolist_error"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "type": "internal_server_error"
        }
    )


# ============================================================================
# ROUTERS
# ============================================================================

# API v1 prefix
API_V1_PREFIX = "/api/v1"

# Register routers
app.include_router(
    projects_router,
    prefix=API_V1_PREFIX,
    tags=["projects"]
)

app.include_router(
    tasks_router,
    prefix=API_V1_PREFIX,
    tags=["tasks"]
)


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get(
    "/",
    tags=["root"],
    summary="API Root",
    description="Welcome endpoint with API information"
)
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Welcome to ToDo List API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "projects": f"{API_V1_PREFIX}/projects",
            "tasks": f"{API_V1_PREFIX}/tasks"
        }
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get(
    "/health",
    tags=["health"],
    summary="Health Check",
    description="Check API health status"
)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "todolist-api"
    }
