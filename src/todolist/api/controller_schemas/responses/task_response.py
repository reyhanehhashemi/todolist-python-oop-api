"""
Task Response Schemas.

Pydantic models for task-related API responses.
"""

from pydantic import BaseModel, Field, field_serializer, ConfigDict
from datetime import datetime
from typing import Optional


class TaskResponse(BaseModel):
    """Task response schema with Tehran timezone."""
    id: int = Field(
        ...,
        description="Task ID",
        examples=[1]
    )
    title: str = Field(
        ...,
        description="Task title",
        examples=["Complete project documentation"]
    )
    description: str = Field(
        ...,
        description="Task description",
        examples=["Write comprehensive API documentation"]
    )
    status: str = Field(
        ...,
        description="Task status (TODO/DOING/DONE)",
        examples=["TODO"]
    )
    deadline: Optional[datetime] = Field(
        default=None,
        description="Task deadline (Tehran time)",
        examples=["2025-12-15 23:59"]
    )
    project_id: int = Field(
        ...,
        description="ID of the project this task belongs to",
        examples=[1]
    )
    closed_at: Optional[datetime] = Field(
        default=None,
        description="Task completion timestamp (Tehran time)",
        examples=["2025-12-10 15:30"]
    )

    @field_serializer('deadline', 'closed_at')
    def serialize_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        """
        فرمت کردن datetime برای JSON response.
        داده از DB به صورت naive Tehran می‌آد، فقط فرمت می‌کنیم.
        """
        if dt is None:
            return None
        return dt.strftime('%Y-%m-%d %H:%M')

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication to the API",
                "status": "DOING",
                "deadline": "2025-12-15 23:59",
                "project_id": 1,
                "closed_at": None
            }
        }
    )
