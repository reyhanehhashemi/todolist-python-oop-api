"""
FastAPI Application Entry Point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..db import init_db
from .routers import api_router

# Import exception handlers
from .exception_handlers import (
    resource_not_found_handler,
    duplicate_resource_handler,
    invalid_operation_handler,
    value_error_handler,
)
from ..utils.exceptions import (
    ResourceNotFoundError,
    DuplicateResourceError,
    InvalidOperationError,
)

# Initialize FastAPI app
app = FastAPI(
    title="TodoList API",
    description="A RESTful API for managing projects and tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Register Custom Exception Handlers
# ============================================================================

app.add_exception_handler(ResourceNotFoundError, resource_not_found_handler)
app.add_exception_handler(DuplicateResourceError, duplicate_resource_handler)
app.add_exception_handler(InvalidOperationError, invalid_operation_handler)
app.add_exception_handler(ValueError, value_error_handler)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    print("✅ Database initialized successfully")


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "ok",
        "message": "TodoList API is running",
        "version": "1.0.0"
    }


# Include API routers
app.include_router(api_router)
