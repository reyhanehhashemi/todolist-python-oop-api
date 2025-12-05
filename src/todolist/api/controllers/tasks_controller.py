"""
Tasks Controller.

Handles all HTTP endpoints related to task management.
"""

from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Optional, List
from datetime import datetime
from enum import Enum
import pytz

from todolist.services.db_task_service import DBTaskService
from todolist.api.dependencies import get_task_service
from todolist.models.task import TaskStatus

# Import schemas from new structure
from ..controller_schemas.requests.task_request import (
    TaskCreateRequest,
    TaskUpdateRequest,
    TaskStatusUpdateRequest
)
from ..controller_schemas.responses.task_response import TaskResponse
from ..controller_schemas.common import ErrorResponse

router = APIRouter()

# تعریف timezone تهران
TEHRAN_TZ = pytz.timezone('Asia/Tehran')


# ✅ اضافه شد: Enum برای محدود کردن فیلدهای مرتب‌سازی
class TaskSortField(str, Enum):
    """Allowed fields for sorting tasks"""
    TITLE = "title"
    DEADLINE = "deadline"


def convert_to_tehran_naive(dt: Optional[datetime]) -> Optional[datetime]:
    """
    تبدیل datetime به Tehran naive (بدون timezone info) برای ذخیره در DB.
    اگر dt از قبل naive باشه، فرض می‌کنیم Tehran هست.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        return dt

    return dt.astimezone(TEHRAN_TZ).replace(tzinfo=None)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={
        400: {"model": ErrorResponse, "description": "Duplicate task title or validation error"},
        404: {"model": ErrorResponse, "description": "Project not found"}
    }
)
async def create_task(
    task: TaskCreateRequest,
    service: DBTaskService = Depends(get_task_service)
):
    """Create task (title unique per project, deadline in Tehran time)"""
    try:
        existing_tasks = service.get_tasks_by_project(task.project_id)
        if any(t.title.lower() == task.title.lower() for t in existing_tasks):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Task with title '{task.title}' already exists in this project"
            )

        description = task.description if task.description else ""
        deadline_tehran = convert_to_tehran_naive(task.deadline)

        return service.create_task(
            title=task.title,
            project_id=task.project_id,
            description=description,
            status=task.status.value,
            deadline=deadline_tehran
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.get(
    "",
    response_model=List[TaskResponse],
    summary="Get all tasks with filtering, pagination and sorting"
)
async def get_all_tasks(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    status: Optional[TaskStatus] = Query(None, description="Filter by status (TODO/DOING/DONE)"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=200, description="Maximum number of records (max 200)"),
    sort_by: TaskSortField = Query(  # ✅ تغییر از Optional[str] به TaskSortField
        TaskSortField.TITLE,  # ✅ پیش‌فرض به title تغییر کرد
        description="Sort field (title or deadline only)"  # ✅ توضیح به‌روز شد
    ),
    order: str = Query(  # ✅ تغییر از Optional[str] به str
        "asc",
        regex="^(asc|desc)$",
        description="Sort order (asc or desc)"
    ),
    service: DBTaskService = Depends(get_task_service)
):
    """
    Get all tasks with advanced filtering, pagination and sorting.

    **Filtering:**
    - project_id: Filter by project
    - status: Filter by status (TODO, DOING, DONE)

    **Pagination:**
    - skip: Offset for pagination (default: 0)
    - limit: Max results per page (default: 100, max: 200)

    **Sorting:**
    - sort_by: Field to sort (title or deadline only)
    - order: Sort direction (asc/desc)

    **Examples:**
    - Get TODO tasks: ?status=TODO
    - Get project 1 tasks: ?project_id=1
    - Pagination: ?skip=0&limit=10
    - Sort by deadline: ?sort_by=deadline&order=desc
    - Combined: ?project_id=1&status=TODO&sort_by=deadline&limit=5
    """
    try:
        tasks = service.get_all_tasks()

        # فیلتر بر اساس project_id
        if project_id is not None:
            tasks = [t for t in tasks if t.project_id == project_id]

        # فیلتر بر اساس status
        if status is not None:
            tasks = [t for t in tasks if t.status == status.value]

        # ✅ مرتب‌سازی - فقط title و deadline
        reverse = (order == "desc")

        if sort_by == TaskSortField.TITLE:  # ✅ مقایسه با Enum
            tasks = sorted(tasks, key=lambda x: x.title.lower(), reverse=reverse)
        elif sort_by == TaskSortField.DEADLINE:  # ✅ مقایسه با Enum
            tasks = sorted(
                tasks,
                key=lambda x: (x.deadline is None, x.deadline or datetime.max),
                reverse=reverse
            )

        # صفحه‌بندی
        tasks = tasks[skip:skip + limit]
        return tasks

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch tasks: {str(e)}"
        )


@router.post(
    "/auto-close-overdue",
    status_code=status.HTTP_200_OK,
    summary="Auto-close overdue tasks"
)
async def auto_close_overdue_tasks(
    service: DBTaskService = Depends(get_task_service)
):
    """
    Manually trigger auto-close operation for overdue tasks.

    This endpoint closes all tasks with TODO or DOING status
    that have passed their deadline.
    """
    try:
        closed_count = service.auto_close_overdue_tasks()
        return {
            "status": "success",
            "message": "Auto-close operation completed",
            "closed_count": closed_count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Auto-close operation failed: {str(e)}"
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def get_task(
    task_id: int,
    service: DBTaskService = Depends(get_task_service)
):
    """Get task by ID (dates displayed in Tehran time)"""
    try:
        return service.get_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        400: {"model": ErrorResponse, "description": "Duplicate task title"}
    }
)
async def update_task(
    task_id: int,
    task: TaskUpdateRequest,
    service: DBTaskService = Depends(get_task_service)
):
    """Update task (all fields optional, deadline in Tehran time)"""
    try:
        existing_task = service.get_task(task_id)

        if task.title and task.title.lower() != existing_task.title.lower():
            project_tasks = service.get_tasks_by_project(existing_task.project_id)
            if any(t.id != task_id and t.title.lower() == task.title.lower() for t in project_tasks):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Task with title '{task.title}' already exists in this project"
                )

        update_data = {}

        if task.title is not None:
            update_data['title'] = task.title

        if task.description is not None:
            update_data['description'] = task.description

        if task.deadline is not None:
            update_data['deadline'] = convert_to_tehran_naive(task.deadline)

        if not update_data:
            return existing_task

        return service.update_task(task_id, **update_data)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error updating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    summary="Quick status update",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdateRequest,
    service: DBTaskService = Depends(get_task_service)
):
    """Quick status update (TODO/DOING/DONE)"""
    try:
        return service.update_task_status(task_id, status_update.status.value)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"Error updating task status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task status: {str(e)}"
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def delete_task(
    task_id: int,
    service: DBTaskService = Depends(get_task_service)
):
    """Delete task"""
    try:
        service.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete task: {str(e)}"
        )


@router.get(
    "/project/{project_id}",
    response_model=List[TaskResponse],
    summary="Get all tasks for a project",
    responses={
        404: {"model": ErrorResponse, "description": "Project not found"}
    }
)
async def get_tasks_by_project(
    project_id: int,
    service: DBTaskService = Depends(get_task_service)
):
    """Get all tasks for a project"""
    try:
        return service.get_tasks_by_project(project_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
