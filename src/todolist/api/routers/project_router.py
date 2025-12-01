"""
Project router for API endpoints.
"""

from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from todolist.api.schemas.project_schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from todolist.services.project_service import DBProjectService
from todolist.api.dependencies import get_project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project"
)
async def create_project(
    project_data: ProjectCreate,
    service: DBProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """
    Create a new project.

    Args:
        project_data: Project creation data
        service: Project service dependency

    Returns:
        Created project
    """
    try:
        project = service.create_project(
            title=project_data.title,
            description=project_data.description
        )
        return ProjectResponse.model_validate(project)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[ProjectResponse],
    summary="Get all projects"
)
async def get_all_projects(
    service: DBProjectService = Depends(get_project_service)
) -> List[ProjectResponse]:
    """
    Get all projects.

    Args:
        service: Project service dependency

    Returns:
        List of all projects
    """
    projects = service.get_all_projects()
    return [ProjectResponse.model_validate(p) for p in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID"
)
async def get_project(
    project_id: str,
    service: DBProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """
    Get a project by ID.

    Args:
        project_id: Project ID
        service: Project service dependency

    Returns:
        Project details
    """
    project = service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return ProjectResponse.model_validate(project)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project"
)
async def update_project(
    project_id: str,
    project_data: ProjectUpdate,
    service: DBProjectService = Depends(get_project_service)
) -> ProjectResponse:
    """
    Update a project.

    Args:
        project_id: Project ID
        project_data: Project update data
        service: Project service dependency

    Returns:
        Updated project
    """
    try:
        project = service.update_project(
            project_id=project_id,
            title=project_data.title,
            description=project_data.description
        )
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {project_id} not found"
            )
        return ProjectResponse.model_validate(project)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete project"
)
async def delete_project(
    project_id: str,
    service: DBProjectService = Depends(get_project_service),
    cascade: bool = True
) -> None:
    """
    Delete a project.

    Args:
        project_id: Project ID
        service: Project service dependency
        cascade: Delete associated tasks (default: True)
    """
    success = service.delete_project(project_id, cascade=cascade)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
