"""
Pydantic schemas for Task API endpoints.
"""
from typing import Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator


def validate_word_count(value: str, max_words: int, field_name: str) -> str:
    """Validate that text doesn't exceed maximum word count."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} cannot be empty")

    word_count = len(value.split())
    if word_count > max_words:
        raise ValueError(
            f"{field_name} exceeds maximum word count. "
            f"Got {word_count} words, maximum is {max_words} words."
        )
    return value


class TaskStatus(str, Enum):
    """Task status enumeration."""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class TaskBase(BaseModel):
    """Base schema for Task."""
    title: str = Field(
        ...,
        description="Task title (maximum 30 words)"
    )
    description: str = Field(
        ...,
        description="Task description (maximum 150 words)"
    )
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        description="Task status (todo, doing, done)"
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Optional task deadline"
    )

    @field_validator('title')
    @classmethod
    def validate_title_words(cls, v: str) -> str:
        """Validate title word count (max 30 words)."""
        return validate_word_count(v, 30, "Title")

    @field_validator('description')
    @classmethod
    def validate_description_words(cls, v: str) -> str:
        """Validate description word count (max 150 words)."""
        return validate_word_count(v, 150, "Description")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    project_id: str = Field(
        ...,
        description="ID of the project this task belongs to"
    )


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(
        None,
        description="Updated task title (optional, max 30 words)"
    )
    description: Optional[str] = Field(
        None,
        description="Updated task description (optional, max 150 words)"
    )
    status: Optional[TaskStatus] = Field(
        None,
        description="Updated task status (optional)"
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Updated task deadline (optional)"
    )

    @field_validator('title')
    @classmethod
    def validate_title_words(cls, v: Optional[str]) -> Optional[str]:
        """Validate title word count if provided."""
        if v is not None:
            return validate_word_count(v, 30, "Title")
        return v

    @field_validator('description')
    @classmethod
    def validate_description_words(cls, v: Optional[str]) -> Optional[str]:
        """Validate description word count if provided."""
        if v is not None:
            return validate_word_count(v, 150, "Description")
        return v


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: str = Field(..., description="Task unique identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    status: TaskStatus = Field(..., description="Task status")
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    project_id: str = Field(..., description="Associated project ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for list of tasks response."""
    tasks: List[TaskResponse]
    total: int = Field(..., description="Total number of tasks")
