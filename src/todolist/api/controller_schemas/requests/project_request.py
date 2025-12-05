"""
Project Request Schemas.

Pydantic models for project-related API requests.
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional


class ProjectCreateRequest(BaseModel):
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


class ProjectUpdateRequest(BaseModel):
    """
    Schema for updating an existing project.

    All fields are optional for partial updates.
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
