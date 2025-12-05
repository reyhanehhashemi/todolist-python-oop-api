"""
Pydantic schemas for Task API endpoints.
"""

from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict
from datetime import datetime
from typing import Optional, Any
from enum import Enum
import pytz


class TaskStatusEnum(str, Enum):
    """Task status enumeration."""
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Task title (1-30 words)",
        examples=["Complete project documentation"]
    )
    description: Optional[str] = Field(
        default="",
        max_length=1500,
        description="Task description (0-150 words, optional)",
        examples=["Write comprehensive API documentation"]
    )
    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the project this task belongs to",
        examples=[1]
    )
    status: TaskStatusEnum = Field(
        default=TaskStatusEnum.TODO,
        description="Initial task status",
        examples=["TODO"]
    )
    deadline: Optional[datetime] = Field(
        default=None,
        description="Task deadline (optional) - Format: YYYY-MM-DD HH:MM (Tehran time)",
        examples=["2025-12-15 23:59"]
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
    def validate_description_word_count(cls, v: Optional[str]) -> str:
        """Validate description does not exceed 150 words."""
        if not v:
            return ""

        words = v.strip().split()
        if len(words) > 150:
            raise ValueError(
                f'Description cannot exceed 150 words. Got {len(words)} words'
            )
        return v.strip()

    @field_validator('deadline', mode='before')
    @classmethod
    def validate_deadline_tehran(cls, v: Any) -> Optional[datetime]:
        """
        Validate deadline is in future (Tehran time).
        """
        if v is None or v == "":
            return None

        if isinstance(v, str):
            try:
                v = datetime.strptime(v, '%Y-%m-%d %H:%M')
            except ValueError:
                try:
                    v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    raise ValueError("Invalid datetime format. Use: YYYY-MM-DD HH:MM")

        tehran_tz = pytz.timezone('Asia/Tehran')
        now_tehran = datetime.now(tehran_tz).replace(tzinfo=None)

        if v <= now_tehran:
            raise ValueError(
                f"Task deadline must be in the future. "
                f"Current time (Tehran): {now_tehran.strftime('%Y-%m-%d %H:%M')}, "
                f"Your deadline: {v.strftime('%Y-%m-%d %H:%M')}"
            )

        return v


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=300,
        description="New task title (optional)",
        examples=["Updated task title"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1500,
        description="New task description (optional)",
        examples=["Updated task description"]
    )
    deadline: Optional[datetime] = Field(
        default=None,
        description="New deadline (optional) - Format: YYYY-MM-DD HH:MM (Tehran time)",
        examples=["2025-12-20 23:59"]
    )

    @field_validator('title')
    @classmethod
    def validate_title_word_count(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Title cannot be empty if provided')
        words = v.strip().split()
        if len(words) > 30:
            raise ValueError(f'Title cannot exceed 30 words. Got {len(words)} words')
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description_word_count(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v:
            return ""
        words = v.strip().split()
        if len(words) > 150:
            raise ValueError(f'Description cannot exceed 150 words. Got {len(words)} words')
        return v.strip()

    @field_validator('deadline', mode='before')
    @classmethod
    def validate_deadline_tehran(cls, v: Any) -> Optional[datetime]:
        if v is None or v == "":
            return None

        if isinstance(v, str):
            try:
                v = datetime.strptime(v, '%Y-%m-%d %H:%M')
            except ValueError:
                try:
                    v = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    raise ValueError("Invalid datetime format. Use: YYYY-MM-DD HH:MM")

        tehran_tz = pytz.timezone('Asia/Tehran')
        now_tehran = datetime.now(tehran_tz).replace(tzinfo=None)

        if v <= now_tehran:
            raise ValueError(
                f"Task deadline must be in the future. "
                f"Current time (Tehran): {now_tehran.strftime('%Y-%m-%d %H:%M')}, "
                f"Your deadline: {v.strftime('%Y-%m-%d %H:%M')}"
            )

        return v


class TaskStatusUpdate(BaseModel):
    """Schema for updating task status only."""
    status: TaskStatusEnum = Field(
        ...,
        description="New task status",
        examples=["DOING"]
    )


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: int
    title: str
    description: str
    status: str
    deadline: Optional[datetime]
    project_id: int
    closed_at: Optional[datetime] = None  # ✅ created_at حذف شد

    @field_serializer('deadline', 'closed_at')  # ✅ created_at حذف شد
    def serialize_datetime(self, dt: Optional[datetime]) -> Optional[str]:
        """
        فقط فرمت می‌کنیم، هیچ تبدیلی نمی‌کنیم.
        DB از اول Tehran ذخیره می‌کنه.
        """
        if dt is None:
            return None
        return dt.strftime('%Y-%m-%d %H:%M')

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Complete documentation",
                "description": "Write comprehensive API documentation",
                "status": "TODO",
                "deadline": "2025-12-15 23:59",
                "project_id": 1,
                "closed_at": None
            }
        }
    )
