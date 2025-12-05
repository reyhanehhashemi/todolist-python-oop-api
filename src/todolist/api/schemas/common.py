"""
Common schemas for API responses.

This module provides shared Pydantic models for error handling
and standard API responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Any, Dict


class ErrorResponse(BaseModel):
    """
    Standard error response schema.

    Used for all error responses across the API.
    """
    detail: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Project with identifier '5' not found"]
    )
    error_code: Optional[str] = Field(
        None,
        description="Machine-readable error code",
        examples=["RESOURCE_NOT_FOUND", "VALIDATION_ERROR"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Project with identifier '5' not found",
                "error_code": "RESOURCE_NOT_FOUND"
            }
        }


class SuccessResponse(BaseModel):
    """
    Standard success response schema.

    Used for operations that don't return specific data.
    """
    message: str = Field(
        ...,
        description="Success message",
        examples=["Project deleted successfully"]
    )
    data: Optional[Dict[str, Any]] = Field(
        None,
        description="Optional additional data"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Project deleted successfully",
                "data": {
                    "project_id": 1,
                    "deleted_tasks": 5
                }
            }
        }


class DeleteResponse(BaseModel):
    """Response schema for delete operations."""
    message: str = Field(
        ...,
        description="Deletion confirmation message"
    )
    deleted_id: int = Field(
        ...,
        description="ID of the deleted resource"
    )
    deleted_tasks: Optional[int] = Field(
        None,
        description="Number of cascade-deleted tasks (for projects)"
    )
