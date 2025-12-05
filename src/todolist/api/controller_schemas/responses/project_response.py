"""
Project Response Schemas.

Pydantic models for project-related API responses.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import List
from ....utils import to_tehran


class TaskStatistics(BaseModel):
    """Statistics about project tasks."""
    total_tasks: int = Field(
        ...,
        description="Total number of tasks",
        examples=[10]
    )
    todo_count: int = Field(
        ...,
        description="Number of TODO tasks",
        examples=[3]
    )
    doing_count: int = Field(
        ...,
        description="Number of DOING tasks",
        examples=[4]
    )
    done_count: int = Field(
        ...,
        description="Number of DONE tasks",
        examples=[3]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_tasks": 10,
                "todo_count": 3,
                "doing_count": 4,
                "done_count": 3
            }
        }
    )


class ProjectResponse(BaseModel):
    """Basic project response schema with Tehran timezone."""
    id: int = Field(
        ...,
        description="Project ID",
        examples=[1]
    )
    title: str = Field(
        ...,
        description="Project title",
        examples=["Personal Development"]
    )
    description: str = Field(
        ...,
        description="Project description",
        examples=["Track my learning goals"]
    )
    created_at: datetime = Field(
        ...,
        description="Project creation timestamp (Tehran time)",
        examples=["2025-12-06T12:52:33"]
    )

    @field_validator('created_at', mode='before')
    @classmethod
    def convert_to_tehran(cls, value):
        """Convert datetime to Tehran timezone."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return to_tehran(value)
        return value

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.replace(tzinfo=None).isoformat() if v else None
        },
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Personal Development",
                "description": "Track my learning goals and progress",
                "created_at": "2025-12-06T12:52:33"
            }
        }
    )


class ProjectDetailResponse(BaseModel):
    """Detailed project response with tasks and statistics."""
    id: int = Field(
        ...,
        description="Project ID",
        examples=[1]
    )
    title: str = Field(
        ...,
        description="Project title",
        examples=["Personal Development"]
    )
    description: str = Field(
        ...,
        description="Project description",
        examples=["Track my learning goals"]
    )
    created_at: datetime = Field(
        ...,
        description="Project creation timestamp (Tehran time)",
        examples=["2025-12-06T12:52:33"]
    )
    tasks: List["TaskResponse"] = Field(
        default_factory=list,
        description="List of all project tasks"
    )
    statistics: TaskStatistics = Field(
        ...,
        description="Task statistics for this project"
    )

    @field_validator('created_at', mode='before')
    @classmethod
    def convert_to_tehran(cls, value):
        """Convert datetime to Tehran timezone."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return to_tehran(value)
        return value

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.replace(tzinfo=None).isoformat() if v else None
        },
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Personal Development",
                "description": "Track my learning goals and progress",
                "created_at": "2025-12-06T12:52:33",
                "tasks": [
                    {
                        "id": 1,
                        "title": "Learn Python",
                        "description": "Complete Python course",
                        "status": "DOING",
                        "deadline": "2025-12-15T23:59:00",
                        "project_id": 1,
                        "closed_at": None
                    }
                ],
                "statistics": {
                    "total_tasks": 10,
                    "todo_count": 3,
                    "doing_count": 4,
                    "done_count": 3
                }
            }
        }
    )


# Import for type hints
from .task_response import TaskResponse
ProjectDetailResponse.model_rebuild()
