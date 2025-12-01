"""
Task API endpoints.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Query

from todolist.api.schemas.task_schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
)
from todolist.api.dependencies import get_task_service
from todolist.services.db_task_service import DBTaskService
from todolist.utils.exceptions import (
    ResourceNotFoundError,
    ValidationError,
)


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task in a specific project.",
)
def create_task(
    task: TaskCreate,
    service: Annotated[DBTaskService, Depends(get_task_service)],
):
    """Create a new task."""
    try:
        created_task = service.create_task(
            title=task.title,
            description=task.description,
            project_id=task.project_id,
            status=task.status,
            deadline=task.deadline,
        )
        return created_task
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="Get all tasks",
    description="Retrieve all tasks, optionally filtered by project and/or status.",
)
def get_all_tasks(
    service: Annotated[DBTaskService, Depends(get_task_service)],
    project_id: int | None = Query(None, description="Filter by project ID"),
    status_filter: str | None = Query(None, description="Filter by status (todo, doing, done)"),
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of tasks to return"),
):
    """Get all tasks with optional filtering and pagination."""
    try:
        if project_id:
            tasks = service.get_tasks_by_project(project_id)
        else:
            tasks = service.get_all_tasks()

        # Filter by status if provided
        if status_filter:
            tasks = [t for t in tasks if t.status == status_filter]

        return tasks[skip : skip + limit]
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Retrieve a specific task by its ID.",
)
def get_task(
    task_id: int,
    service: Annotated[DBTaskService, Depends(get_task_service)],
):
    """Get a task by ID."""
    try:
        task = service.get_task(task_id)
        return task
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update task details including title, description, status, deadline, or project.",
)
def update_task(
    task_id: int,
    task: TaskUpdate,
    service: Annotated[DBTaskService, Depends(get_task_service)],
):
    """Update a task."""
    try:
        updated_task = service.update_task(
            task_id=task_id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
            project_id=task.project_id,
        )
        return updated_task
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a specific task by its ID.",
)
def delete_task(
    task_id: int,
    service: Annotated[DBTaskService, Depends(get_task_service)],
):
    """Delete a task."""
    try:
        service.delete_task(task_id)
        return None
    except ResourceNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
