"""
Global Exception Handlers for FastAPI.

Handles custom exceptions and converts them to appropriate HTTP responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse

from ..utils.exceptions import (
    ResourceNotFoundError,
    DuplicateResourceError,
    InvalidOperationError,
)


async def resource_not_found_handler(
        request: Request,
        exc: ResourceNotFoundError
) -> JSONResponse:
    """
    Handle ResourceNotFoundError → 404 Not Found.

    Example:
        Task with ID '20' not found → 404
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
            "path": str(request.url)
        }
    )


async def duplicate_resource_handler(
        request: Request,
        exc: DuplicateResourceError
) -> JSONResponse:
    """
    Handle DuplicateResourceError → 409 Conflict.

    Example:
        Project with title 'MyProject' already exists → 409
    """
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
            "path": str(request.url)
        }
    )


async def invalid_operation_handler(
        request: Request,
        exc: InvalidOperationError
) -> JSONResponse:
    """
    Handle InvalidOperationError → 400 Bad Request.

    Example:
        Cannot delete project with active tasks → 400
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "path": str(request.url)
        }
    )


# Optional: Handle generic ValueError (fallback)
async def value_error_handler(
        request: Request,
        exc: ValueError
) -> JSONResponse:
    """
    Handle generic ValueError → 400 Bad Request.

    This catches any ValueError that wasn't caught by other handlers.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": str(exc),
            "path": str(request.url)
        }
    )
