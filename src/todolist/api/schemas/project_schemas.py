"""
Project API schemas using Pydantic v2.
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ProjectBase(BaseModel):
    """Base schema for project with common fields."""

    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Project title (3-100 characters)",
        json_schema_extra={"examples": ["My First Project"]}
    )
    description: str | None = Field(
        None,
        max_length=500,
        description="Project description (optional, max 500 characters)",
        json_schema_extra={"examples": ["This is a project for managing tasks"]}
    )


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    title: str | None = Field(
        None,
        min_length=3,
        max_length=100,
        description="Updated project title",
    )
    description: str | None = Field(
        None,
        max_length=500,
        description="Updated project description",
    )


class ProjectResponse(ProjectBase):
    """Schema for project response."""

    id: int = Field(..., description="Project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class TaskSummary(BaseModel):
    """Summary of tasks in a project."""

    total: int = Field(..., description="Total number of tasks")
    todo: int = Field(..., description="Number of tasks with 'todo' status")
    doing: int = Field(..., description="Number of tasks with 'doing' status")
    done: int = Field(..., description="Number of tasks with 'done' status")


class ProjectSummaryResponse(ProjectResponse):
    """Extended project response with task statistics."""

    task_summary: TaskSummary = Field(..., description="Task statistics")


class ProjectDeleteResponse(BaseModel):
    """Response for project deletion."""

    message: str = Field(..., description="Deletion confirmation message")
    deleted_tasks_count: int = Field(
        ...,
        description="Number of tasks deleted (if cascade=True)"
    )
