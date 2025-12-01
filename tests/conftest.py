"""
Pytest configuration and shared fixtures.
"""

import pytest
from src.todolist.repositories.project_repository import ProjectRepository
from src.todolist.repositories.task_repository import TaskRepository
from src.todolist.services.project_service import ProjectService
from src.todolist.services.task_service import TaskService
from src.todolist.models.project import Project
from src.todolist.models.task import Task
from src.todolist.utils.id_generator import id_generator


@pytest.fixture(autouse=True)
def reset_id_generator():
    """Reset ID generator before each test."""
    id_generator.reset()
    yield
    id_generator.reset()


@pytest.fixture
def project_repo():
    """Provide a fresh project repository."""
    return ProjectRepository()


@pytest.fixture
def task_repo():
    """Provide a fresh task repository."""
    return TaskRepository()


@pytest.fixture
def project_service(project_repo, task_repo):
    """Provide a project service with repositories."""
    return ProjectService(project_repo, task_repo)


@pytest.fixture
def task_service(task_repo):
    """Provide a task service with repository."""
    return TaskService(task_repo)


@pytest.fixture
def sample_project():
    """Provide a sample project."""
    return Project(title="Test Project", description="Test Description")


@pytest.fixture
def sample_task(sample_project):
    """Provide a sample task."""
    return Task(
        title="Test Task",
        project_id=sample_project.id,
        description="Test task description",
    )
