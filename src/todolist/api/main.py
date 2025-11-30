"""
FastAPI application for TodoList.
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from todolist.api.routers import project_router, task_router
from todolist.utils.exceptions import (
    TodoListException,
    ValidationError,
    ProjectNotFoundError,
    MaxProjectsReachedError,
    TaskNotFoundError,
    MaxTasksReachedError
)


# Initialize FastAPI app
app = FastAPI(
    title="TodoList API",
    description="A RESTful API for managing projects and tasks",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(TodoListException)
async def todolist_exception_handler(request: Request, exc: TodoListException):
    """Handle custom TodoList exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)}
    )


@app.exception_handler(ProjectNotFoundError)
@app.exception_handler(TaskNotFoundError)
async def not_found_exception_handler(request: Request, exc: Exception):
    """Handle not found errors."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


@app.exception_handler(MaxProjectsReachedError)
@app.exception_handler(MaxTasksReachedError)
async def max_reached_exception_handler(request: Request, exc: Exception):
    """Handle max limit errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


# Include routers
app.include_router(project_router.router, prefix="/api/v1")
app.include_router(task_router.router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to TodoList API",
        "version": "3.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "api_version": "3.0.0"
    }
