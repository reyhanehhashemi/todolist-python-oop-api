"""
Pydantic schemas for Project API endpoints.

This module defines request and response models for project-related
operations with comprehensive validation rules.
"""

from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict
from datetime import datetime
from typing import Optional
import pytz


class ProjectCreate(BaseModel):
    """
    Schema for creating a new project.

    Validates:
    - Title: 1-30 words, max 300 characters
    - Description: 0-150 words, max 1500 characters
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Project title (1-30 words)",
        examples=["Personal Task Management"]
    )
    description: str = Field(
        default="",
        max_length=1500,
        description="Project description (0-150 words, optional)",
        examples=["A project to organize daily personal tasks"]
    )

    @field_validator('title')
    @classmethod
    def validate_title_word_count(cls, v: str) -> str:
        """Validate title does not exceed 30 words."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')

        words = v.strip().split()
        if len(words) > 30:
            raise ValueError(
                f'Title cannot exceed 30 words. Got {len(words)} words'
            )
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description_word_count(cls, v: str) -> str:
        """Validate description does not exceed 150 words."""
        if not v:
            return ""

        words = v.strip().split()
        if len(words) > 150:
            raise ValueError(
                f'Description cannot exceed 150 words. Got {len(words)} words'
            )
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Personal Development",
                "description": "Track my learning goals and progress"
            }
        }
    )


class ProjectUpdate(BaseModel):
    """
    Schema for updating an existing project.

    All fields are optional for partial updates (PATCH).
    """
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=300,
        description="New project title (optional)",
        examples=["Updated Project Name"]
    )
    description: Optional[str] = Field(
        None,
        max_length=1500,
        description="New project description (optional)",
        examples=["Updated description with more details"]
    )

    @field_validator('title')
    @classmethod
    def validate_title_word_count(cls, v: Optional[str]) -> Optional[str]:
        """Validate title if provided."""
        if v is None:
            return v

        if not v.strip():
            raise ValueError('Title cannot be empty if provided')

        words = v.strip().split()
        if len(words) > 30:
            raise ValueError(
                f'Title cannot exceed 30 words. Got {len(words)} words'
            )
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description_word_count(cls, v: Optional[str]) -> Optional[str]:
        """Validate description if provided."""
        if v is None:
            return v

        if not v:
            return ""

        words = v.strip().split()
        if len(words) > 150:
            raise ValueError(
                f'Description cannot exceed 150 words. Got {len(words)} words'
            )
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Updated Project Name",
                "description": "Updated project description"
            }
        }
    )


class ProjectResponse(BaseModel):
    """
    Schema for project response.

    Returned by GET, POST, PUT, PATCH endpoints.
    """
    id: int = Field(
        ...,
        description="Unique project identifier",
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
        examples=["Track learning goals"]
    )
    created_at: datetime = Field(
        ...,
        description="Project creation timestamp"
    )

    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime) -> str:
        """Convert UTC to Tehran timezone and format as YYYY-MM-DD HH:MM"""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=pytz.UTC)
        tehran_tz = pytz.timezone('Asia/Tehran')
        dt_tehran = dt.astimezone(tehran_tz)
        return dt_tehran.strftime('%Y-%m-%d %H:%M')

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Personal Development",
                "description": "Track my learning goals",
                "created_at": "2025-12-01 10:30"
            }
        }
    )


class TaskStatistics(BaseModel):
    """Task count statistics for a project."""
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
        examples=[5]
    )
    done_count: int = Field(
        ...,
        description="Number of DONE tasks",
        examples=[2]
    )


class ProjectDetailResponse(ProjectResponse):
    """
    Extended project response with tasks and statistics.

    Includes:
    - All project fields (id, title, description, created_at)
    - List of all tasks in this project
    - Task count statistics by status
    """
    tasks: list['TaskResponse'] = Field(
        default_factory=list,
        description="List of all tasks in this project"
    )
    statistics: TaskStatistics = Field(
        ...,
        description="Task statistics for this project"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Personal Development",
                "description": "Track learning goals",
                "created_at": "2025-12-01 10:30",
                "tasks": [
                    {
                        "id": 1,
                        "title": "Learn FastAPI",
                        "description": "Complete FastAPI tutorial",
                        "status": "DOING",
                        "deadline": "2025-12-15 23:59",
                        "project_id": 1,
                        "created_at": "2025-12-01 10:30",
                        "closed_at": None
                    }
                ],
                "statistics": {
                    "total_tasks": 10,
                    "todo_count": 3,
                    "doing_count": 5,
                    "done_count": 2
                }
            }
        }
    )


class ProjectList(BaseModel):
    """Response schema for listing projects."""
    projects: list[ProjectResponse] = Field(
        ...,
        description="List of projects"
    )
    total: int = Field(
        ...,
        description="Total number of projects"
    )


# Import TaskResponse برای استفاده در ProjectDetailResponse
from todolist.api.schemas.task import TaskResponse
ProjectDetailResponse.model_rebuild()
