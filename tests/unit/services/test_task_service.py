"""
Unit tests for TaskService.
"""

import pytest
from datetime import datetime, timedelta
from src.todolist.services.task_service import TaskService
from src.todolist.models.task import TaskStatus
from src.todolist.utils.exceptions import ResourceNotFoundError, ValidationError


class TestTaskService:
    """Test TaskService functionality."""

    def test_create_task(self, task_service, sample_project):
        """Test creating a task through service."""
        task = task_service.create_task(
            title="Service Task",
            project_id=sample_project.id,
            description="Created via service",
        )

        assert task.title == "Service Task"
        assert task.project_id == sample_project.id
        assert task.status == TaskStatus.TODO.value
        assert task.deadline is None

    def test_create_task_invalid_title(self, task_service, sample_project):
        """Test creating task with empty title raises error."""
        with pytest.raises(ValidationError):
            task_service.create_task(title="", project_id=sample_project.id)

    def test_get_task(self, task_service, sample_project):
        """Test retrieving a task."""
        created = task_service.create_task("Test", sample_project.id)
        retrieved = task_service.get_task(created.id)

        assert retrieved.id == created.id

    def test_get_task_not_found(self, task_service):
        """Test retrieving non-existent task raises error."""
        with pytest.raises(ResourceNotFoundError):
            task_service.get_task(999999)

    def test_get_tasks_by_project(self, task_service, sample_project):
        """Test getting tasks by project."""
        task_service.create_task("Task 1", sample_project.id)
        task_service.create_task("Task 2", sample_project.id)

        tasks = task_service.get_tasks_by_project(sample_project.id)

        assert len(tasks) == 2

    def test_update_task(self, task_service, sample_project):
        """Test updating task details."""
        task = task_service.create_task("Original", sample_project.id)

        updated = task_service.update_task(
            task.id, title="Updated", description="New desc"
        )

        assert updated.title == "Updated"
        assert updated.description == "New desc"

    def test_update_task_status(self, task_service, sample_project):
        """Test updating task status."""
        task = task_service.create_task("Test", sample_project.id)

        updated = task_service.update_task_status(task.id, TaskStatus.DONE.value)

        assert updated.status == TaskStatus.DONE.value

    def test_update_task_status_invalid(self, task_service, sample_project):
        """Test updating to invalid status raises error."""
        task = task_service.create_task("Test", sample_project.id)

        with pytest.raises(ValidationError):
            task_service.update_task_status(task.id, "INVALID")

    def test_delete_task(self, task_service, sample_project):
        """Test deleting a task."""
        task = task_service.create_task("Test", sample_project.id)
        task_service.delete_task(task.id)

        with pytest.raises(ResourceNotFoundError):
            task_service.get_task(task.id)

    def test_get_tasks_by_status(self, task_service, sample_project):
        """Test filtering tasks by status."""
        task1 = task_service.create_task("Task 1", sample_project.id)
        task2 = task_service.create_task("Task 2", sample_project.id)
        task_service.update_task_status(task2.id, TaskStatus.DONE.value)

        todo_tasks = task_service.get_tasks_by_status(TaskStatus.TODO.value)
        done_tasks = task_service.get_tasks_by_status(TaskStatus.DONE.value)

        assert len(todo_tasks) == 1
        assert len(done_tasks) == 1

    # New deadline tests
    def test_create_task_with_deadline(self, task_service, sample_project):
        """Test creating task with deadline."""
        future_deadline = datetime.now() + timedelta(days=7)
        task = task_service.create_task(
            title="Task with deadline",
            project_id=sample_project.id,
            deadline=future_deadline
        )

        assert task.deadline == future_deadline

    def test_create_task_with_past_deadline(self, task_service, sample_project):
        """Test creating task with past deadline raises error."""
        past_deadline = datetime.now() - timedelta(days=1)

        with pytest.raises(ValidationError, match="cannot be in the past"):
            task_service.create_task(
                title="Task with past deadline",
                project_id=sample_project.id,
                deadline=past_deadline
            )

    def test_update_task_deadline(self, task_service, sample_project):
        """Test updating task deadline."""
        task = task_service.create_task("Test Task", sample_project.id)
        future_deadline = datetime.now() + timedelta(days=5)

        updated = task_service.update_task(task.id, deadline=future_deadline)

        assert updated.deadline == future_deadline

    def test_update_task_with_past_deadline(self, task_service, sample_project):
        """Test updating task with past deadline raises error."""
        task = task_service.create_task("Test Task", sample_project.id)
        past_deadline = datetime.now() - timedelta(hours=2)

        with pytest.raises(ValidationError, match="cannot be in the past"):
            task_service.update_task(task.id, deadline=past_deadline)
