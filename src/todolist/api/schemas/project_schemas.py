"""
Pydantic schemas for Project API endpoints.
"""
from typing import Optional, List
from datetime import datetime
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


class ProjectBase(BaseModel):
    """Base schema for Project."""
    name: str = Field(
        ...,
        min_length=3,
        description="Project name (minimum 3 characters, unique)"
    )
    description: str = Field(
        ...,
        description="Project description (maximum 150 words)"
    )

    @field_validator('name')
    @classmethod
    def validate_name_length(cls, v: str) -> str:
        """Validate project name length."""
        if len(v) < 3:
            raise ValueError("Project name must be at least 3 characters")
        return v

    @field_validator('description')
    @classmethod
    def validate_description_words(cls, v: str) -> str:
        """Validate description word count (max 150 words)."""
        return validate_word_count(v, 150, "Description")


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""
    name: Optional[str] = Field(
        None,
        min_length=3,
        description="Updated project name (optional)"
    )
    description: Optional[str] = Field(
        None,
        description="Updated project description (optional, max 150 words)"
    )

    @field_validator('name')
    @classmethod
    def validate_name_length(cls, v: Optional[str]) -> Optional[str]:
        """Validate project name length if provided."""
        if v is not None and len(v) < 3:
            raise ValueError("Project name must be at least 3 characters")
        return v

    @field_validator('description')
    @classmethod
    def validate_description_words(cls, v: Optional[str]) -> Optional[str]:
        """Validate description word count if provided."""
        if v is not None:
            return validate_word_count(v, 150, "Description")
        return v


class ProjectResponse(ProjectBase):
    """Schema for project response."""
    id: str = Field(..., description="Project unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Schema for list of projects response."""
    projects: List[ProjectResponse]
    total: int = Field(..., description="Total number of projects")
