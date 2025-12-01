"""
FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from todolist.api.routers import project_router, task_router
from todolist.config.settings import settings


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="ToDoList API",
        description="RESTful API for ToDoList application",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify allowed origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(project_router.router, prefix="/api/v1")
    app.include_router(task_router.router, prefix="/api/v1")

    @app.get("/")
    def root():
        """Root endpoint."""
        return {
            "message": "ToDoList API",
            "version": "1.0.0",
            "docs": "/api/docs",
        }

    @app.get("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}

    return app


app = create_app()
