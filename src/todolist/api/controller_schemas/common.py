"""
Common schemas shared across the API.
"""

from pydantic import BaseModel, Field, ConfigDict


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    detail: str = Field(
        ...,
        description="Error message",
        examples=["Resource not found"]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Project with ID 123 not found"
            }
        }
    )
