from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from todolist.api.dependencies import get_db, get_project_service
from todolist.api.schemas.project_schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
)
from todolist.services.project_service import ProjectService
from todolist.utils.exceptions import (
    ProjectNotFoundError,
    MaxProjectsReachedError,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "/",
    response_model=ProjectResponse,  # ✅ اینجا تعریف می‌کنیم
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new project with title and description",
)
async def create_project(
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):  # ✅ Return Type رو حذف می‌کنیم
    """
    Create a new project.

    Args:
        project: Project creation data
        service: Project service instance
        db: Database session

    Returns:
        Created project

    Raises:
        HTTPException 400: Max projects limit reached
    """
    try:
        created_project = service.create_project(
            title=project.title,
            description=project.description,
        )
        return created_project
    except MaxProjectsReachedError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[ProjectResponse],  # ✅ لیست از ProjectResponse
    summary="Get all projects",
    description="Retrieve all projects",
)
async def get_projects(
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    """Get all projects."""
    return service.get_all_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,  # ✅ اینجا تعریف می‌کنیم
    summary="Get project by ID",
    description="Retrieve a specific project by its ID",
)
async def get_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    """
    Get project by ID.

    Args:
        project_id: Project ID
        service: Project service instance
        db: Database session

    Returns:
        Project data

    Raises:
        HTTPException 404: Project not found
    """
    try:
        return service.get_project(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,  # ✅ اینجا تعریف می‌کنیم
    summary="Update project",
    description="Update an existing project",
)
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    """
    Update project.

    Args:
        project_id: Project ID
        project: Project update data
        service: Project service instance
        db: Database session

    Returns:
        Updated project

    Raises:
        HTTPException 404: Project not found
    """
    try:
        updated_project = service.update_project(
            project_id=project_id,
            title=project.title,
            description=project.description,
        )
        return updated_project
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project",
    description="Delete a project and all its tasks",
)
async def delete_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service),
    db: Session = Depends(get_db),
):
    """
    Delete project.

    Args:
        project_id: Project ID
        service: Project service instance
        db: Database session

    Raises:
        HTTPException 404: Project not found
    """
    try:
        service.delete_project(project_id)
        return None  # ✅ 204 No Content
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
