from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from todolist.api.dependencies import get_db, get_task_service
from todolist.api.schemas.task_schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
)
from todolist.services.task_service import TaskService
from todolist.utils.exceptions import (
    TaskNotFoundError,
    ProjectNotFoundError,
    MaxTasksReachedError,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskResponse,  # ✅ اینجا تعریف می‌کنیم
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task in a project",
)
async def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
    db: Session = Depends(get_db),
):
    """
    Create a new task.

    Args:
        task: Task creation data
        service: Task service instance
        db: Database session

    Returns:
        Created task

    Raises:
        HTTPException 400: Max tasks limit reached
        HTTPException 404: Project not found
    """
    try:
        created_task = service.create_task(
            title=task.title,
            description=task.description,
            project_id=task.project_id,
            deadline=task.deadline,
        )
        return created_task
    except MaxTasksReachedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[TaskResponse],  # ✅ لیست از TaskResponse
    summary="Get all tasks",
    description="Retrieve tasks with optional filtering",
)
async def get_tasks(
    project_id: Optional[str] = Query(None, description="Filter by project ID"),
    status: Optional[str] = Query(None, description="Filter by task status"),
    service: TaskService = Depends(get_task_service),
    db: Session = Depends(get_db),
):
    """Get all tasks with optional filters."""
    if project_id:
        return service.get_tasks_by_project(project_id)
    elif status:
        return service.get_tasks_by_status(status)
    else:
        return service.get_all_tasks()


@router.get(
    "/{task_id}",
    response_model=TaskResponse,  # ✅ اینجا تعریف می‌کنیم
    summary="Get task by ID",
    description="Retrieve a specific task by its ID",
)
async def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    db: Session = Depends(get_db),
):
    """
    Get task by ID.

    Args:
        task_id: Task ID
        service: Task service instance
        db: Database session

    Returns:
        Task data

    Raises:
        HTTPException 404: Task not found
    """
    try:
        return service.get_task(task_id)
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,  # ✅ اینجا تعریف می‌کنیم
    summary="Update task",
    description="Update an existing task",
)
async def update_task(
    task_id: str,
    task: TaskUpdate,
    service: TaskService = Depends(get_task_service),
    db: Session = Depends(get_db),
):
    """
    Update task.

    Args:
        task_id: Task ID
        task: Task update data
        service: Task service instance
        db: Database session

    Returns:
        Updated task

    Raises:
        HTTPException 404: Task not found
    """
    try:
        updated_task = service.update_task(
            task_id=task_id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
        )
        return updated_task
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete a task",
)
async def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    db: Session = Depends(get_db),
):
    """
    Delete task.

    Args:
        task_id: Task ID
        service: Task service instance
        db: Database session

    Raises:
        HTTPException 404: Task not found
    """
    try:
        service.delete_task(task_id)
        return None  # ✅ 204 No Content
    except TaskNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
