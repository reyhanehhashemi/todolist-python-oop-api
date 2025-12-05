from fastapi import APIRouter, HTTPException, Depends, status
from todolist.api.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectDetailResponse,
    TaskStatistics,
    TaskResponse,
    ErrorResponse
)
from todolist.services.db_project_service import DBProjectService
from todolist.services.db_task_service import DBTaskService
from todolist.api.dependencies import get_project_service, get_task_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
        project: ProjectCreate,
        service: DBProjectService = Depends(get_project_service)
):
    """Create new project (title must be unique)"""
    try:
        existing_projects = service.get_all_projects()
        if any(p.title.lower() == project.title.lower() for p in existing_projects):
            raise HTTPException(
                status_code=400,
                detail=f"Project with title '{project.title}' already exists"
            )

        description = project.description if project.description else ""
        return service.create_project(project.title, description)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")


@router.get("/", response_model=list[ProjectResponse])
def get_all_projects(
        service: DBProjectService = Depends(get_project_service)
):
    """Get all projects"""
    return service.get_all_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectDetailResponse,
    summary="Get project details with tasks and statistics",
    responses={
        404: {"model": ErrorResponse, "description": "Project not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def get_project_details(
        project_id: int,
        project_service: DBProjectService = Depends(get_project_service),
        task_service: DBTaskService = Depends(get_task_service)
):
    """Get project with all tasks and statistics (total, todo, doing, done)"""
    try:
        # Get project
        project = project_service.get_project(project_id)

        # Get project tasks
        all_tasks = task_service.get_all_tasks()
        project_tasks = [t for t in all_tasks if t.project_id == project_id]

        # Convert to TaskResponse
        tasks_list = []
        for task in project_tasks:
            tasks_list.append(TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description or "",
                status=task.status.value if hasattr(task.status, 'value') else task.status,
                deadline=task.deadline,
                project_id=task.project_id,
                created_at=task.created_at,
                closed_at=getattr(task, 'closed_at', None)
            ))

        # Calculate statistics
        todo_count = sum(1 for t in tasks_list if t.status == 'TODO')
        doing_count = sum(1 for t in tasks_list if t.status == 'DOING')
        done_count = sum(1 for t in tasks_list if t.status == 'DONE')

        return ProjectDetailResponse(
            id=project.id,
            title=project.title,
            description=project.description or "",
            created_at=project.created_at,
            tasks=tasks_list,
            statistics=TaskStatistics(
                total_tasks=len(tasks_list),
                todo_count=todo_count,
                doing_count=doing_count,
                done_count=done_count
            )
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    except Exception as e:
        print(f"Error retrieving project details: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving project details: {str(e)}"
        )


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
        project_id: int,
        project: ProjectUpdate,
        service: DBProjectService = Depends(get_project_service)
):
    """Update project (all fields optional)"""
    try:
        existing_project = service.get_project(project_id)

        new_title = project.title if project.title is not None else existing_project.title
        new_description = project.description if project.description is not None else existing_project.description

        if project.title and project.title.lower() != existing_project.title.lower():
            existing_projects = service.get_all_projects()
            if any(p.id != project_id and p.title.lower() == project.title.lower() for p in existing_projects):
                raise HTTPException(
                    status_code=400,
                    detail=f"Project with title '{project.title}' already exists"
                )

        return service.update_project(project_id, new_title, new_description)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update project: {str(e)}")


@router.delete("/{project_id}", status_code=204)
def delete_project(
        project_id: int,
        service: DBProjectService = Depends(get_project_service)
):
    """Delete project"""
    try:
        service.delete_project(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")
