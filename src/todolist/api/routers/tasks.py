from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from datetime import datetime
import pytz
from todolist.api.schemas import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate
from todolist.services.db_task_service import DBTaskService
from todolist.api.dependencies import get_task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

# تعریف timezone تهران
TEHRAN_TZ = pytz.timezone('Asia/Tehran')


def convert_to_tehran_naive(dt: Optional[datetime]) -> Optional[datetime]:
    """
    تبدیل datetime به Tehran naive (بدون timezone info) برای ذخیره در DB.
    اگر dt از قبل naive باشه، فرض می‌کنیم Tehran هست.
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        # اگر naive باشه، فرض می‌کنیم Tehran هست
        return dt

    # اگر aware باشه، به Tehran تبدیل و naive می‌کنیم
    return dt.astimezone(TEHRAN_TZ).replace(tzinfo=None)


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
        task: TaskCreate,
        service: DBTaskService = Depends(get_task_service)
):
    """Create task (title unique per project, deadline in Tehran time)"""
    try:
        # Check duplicate title in same project
        existing_tasks = service.get_tasks_by_project(task.project_id)
        if any(t.title.lower() == task.title.lower() for t in existing_tasks):
            raise HTTPException(
                status_code=400,
                detail=f"Task with title '{task.title}' already exists in this project"
            )

        description = task.description if task.description else ""

        # 🔥 تبدیل deadline به Tehran naive قبل از ارسال به service
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
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks(
        project_id: Optional[int] = Query(None, description="Filter by project ID"),
        service: DBTaskService = Depends(get_task_service)
):
    """Get all tasks (optional filter by project)"""
    if project_id:
        return service.get_tasks_by_project(project_id)
    return service.get_all_tasks()


@router.post("/auto-close-overdue", status_code=200)
def auto_close_overdue_tasks(
        service: DBTaskService = Depends(get_task_service)
):
    """
    Manually trigger auto-close operation for overdue tasks.

    This endpoint closes all tasks with TODO or DOING status
    that have passed their deadline. The same operation runs
    automatically via cron job (legacy CLI support maintained).

    Returns closed_count indicating number of tasks that were closed.
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
            status_code=500,
            detail=f"Auto-close operation failed: {str(e)}"
        )


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
        task_id: int,
        service: DBTaskService = Depends(get_task_service)
):
    """Get task by ID (dates displayed in Tehran time)"""
    try:
        return service.get_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
        task_id: int,
        task: TaskUpdate,
        service: DBTaskService = Depends(get_task_service)
):
    """Update task (all fields optional, deadline in Tehran time)"""
    try:
        # Get current task
        existing_task = service.get_task(task_id)

        # Check duplicate title if changed
        if task.title and task.title.lower() != existing_task.title.lower():
            project_tasks = service.get_tasks_by_project(existing_task.project_id)
            if any(t.id != task_id and t.title.lower() == task.title.lower() for t in project_tasks):
                raise HTTPException(
                    status_code=400,
                    detail=f"Task with title '{task.title}' already exists in this project"
                )

        # Prepare update data
        update_data = {}

        if task.title is not None:
            update_data['title'] = task.title

        if task.description is not None:
            update_data['description'] = task.description

        if task.deadline is not None:
            # 🔥 تبدیل deadline به Tehran naive قبل از ارسال به service
            update_data['deadline'] = convert_to_tehran_naive(task.deadline)

        # If nothing to update, return existing task
        if not update_data:
            return existing_task

        return service.update_task(task_id, **update_data)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
        task_id: int,
        status_update: TaskStatusUpdate,
        service: DBTaskService = Depends(get_task_service)
):
    """Quick status update (TODO/DOING/DONE)"""
    try:
        return service.update_task_status(task_id, status_update.status.value)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Error updating task status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update task status: {str(e)}")


@router.delete("/{task_id}", status_code=204)
def delete_task(
        task_id: int,
        service: DBTaskService = Depends(get_task_service)
):
    """Delete task"""
    try:
        service.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")


@router.get("/project/{project_id}", response_model=list[TaskResponse])
def get_tasks_by_project(
        project_id: int,
        service: DBTaskService = Depends(get_task_service)
):
    """Get all tasks for a project"""
    try:
        return service.get_tasks_by_project(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
