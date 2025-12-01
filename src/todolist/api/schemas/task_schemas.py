"""
Task API schemas using Pydantic v2.
"""

from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Literal


class TaskBase(BaseModel):
    """Base schema for task with common fields."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=30,
        description="Task title (1-30 characters)",
        json_schema_extra={"examples": ["Complete homework"]}
    )
    description: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Task description (1-150 characters)",
        json_schema_extra={"examples": ["Finish math assignment by Friday"]}
    )
    status: Literal["todo", "doing", "done"] = Field(
        default="todo",
        description="Task status (todo, doing, done)"
    )
    deadline: date | None = Field(
        None,
        description="Task deadline (optional, YYYY-MM-DD format)",
        json_schema_extra={"examples": ["2025-12-15"]}
    )


class TaskCreate(TaskBase):
    """Schema for creating a new task."""

    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the project this task belongs to"
    )


class TaskUpdate(BaseModel):
    """Schema for updating a task."""

    title: str | None = Field(
        None,
        min_length=1,
        max_length=30,
        description="Updated task title",
    )
    description: str | None = Field(
        None,
        min_length=1,
        max_length=150,
        description="Updated task description",
    )
    status: Literal["todo", "doing", "done"] | None = Field(
        None,
        description="Updated task status"
    )
    deadline: date | None = Field(
        None,
        description="Updated task deadline"
    )
    project_id: int | None = Field(
        None,
        gt=0,
        description="Move task to different project"
    )


class TaskResponse(TaskBase):
    """Schema for task response."""

    id: int = Field(..., description="Task ID")
    project_id: int = Field(..., description="Project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Schema for paginated task list."""

    tasks: list[TaskResponse] = Field(..., description="List of tasks")
    total: int = Field(..., description="Total number of tasks")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
