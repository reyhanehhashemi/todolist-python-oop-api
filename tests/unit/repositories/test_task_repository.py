"""
Unit tests for TaskRepository.
"""

import pytest
from src.todolist.models.task import Task
from src.todolist.repositories.task_repository import TaskRepository
from src.todolist.utils.exceptions import ResourceNotFoundError


class TestTaskRepository:
    """Test suite for TaskRepository."""

    def test_add_task(self, task_repo, sample_task):
        """Test adding a task."""
        added = task_repo.add(sample_task)
        assert added.id == sample_task.id
        assert task_repo.count() == 1

    def test_get_by_id_exists(self, task_repo, sample_task):
        """Test getting task by ID when it exists."""
        task_repo.add(sample_task)
        retrieved = task_repo.get_by_id(sample_task.id)
        assert retrieved.id == sample_task.id
        assert retrieved.title == sample_task.title

    def test_get_by_id_not_exists(self, task_repo):
        """Test getting task by ID when it doesn't exist."""
        with pytest.raises(ResourceNotFoundError):
            task_repo.get_by_id(999)

    def test_get_all_empty(self, task_repo):
        """Test getting all tasks when repository is empty."""
        tasks = task_repo.get_all()
        assert len(tasks) == 0

    def test_get_all_multiple(self, task_repo):
        """Test getting all tasks with multiple tasks."""
        task1 = Task(title="Task 1", project_id=1)
        task2 = Task(title="Task 2", project_id=1)
        task_repo.add(task1)
        task_repo.add(task2)

        tasks = task_repo.get_all()
        assert len(tasks) == 2

    def test_get_by_project_id(self, task_repo, sample_project):
        """Test getting tasks by project ID."""
        project_id = sample_project.id
        task1 = Task(title="Task 1", project_id=project_id)
        task2 = Task(title="Task 2", project_id=project_id)
        task3 = Task(title="Task 3", project_id=999)  # Different project

        task_repo.add(task1)
        task_repo.add(task2)
        task_repo.add(task3)

        project_tasks = task_repo.get_by_project_id(project_id)
        assert len(project_tasks) == 2
        assert all(t.project_id == project_id for t in project_tasks)

    def test_update_task(self, task_repo, sample_task):
        """Test updating a task."""
        task_repo.add(sample_task)
        sample_task.title = "Updated Title"
        updated = task_repo.update(sample_task)
        assert updated.title == "Updated Title"

    def test_update_non_existent(self, task_repo):
        """Test updating non-existent task raises error."""
        task = Task(title="Test", project_id=1)
        # Don't add the task, just try to update
        with pytest.raises(ResourceNotFoundError):
            task_repo.update(task)

    def test_delete_task(self, task_repo, sample_task):
        """Test deleting a task."""
        task_repo.add(sample_task)
        task_repo.delete(sample_task.id)
        assert task_repo.count() == 0

    def test_delete_non_existent(self, task_repo):
        """Test deleting non-existent task raises error."""
        with pytest.raises(ResourceNotFoundError):
            task_repo.delete(999)

    def test_delete_by_project_id(self, task_repo, sample_project):
        """Test cascade delete by project ID."""
        project_id = sample_project.id
        task1 = Task(title="Task 1", project_id=project_id)
        task2 = Task(title="Task 2", project_id=project_id)
        task3 = Task(title="Task 3", project_id=999)  # Different project

        task_repo.add(task1)
        task_repo.add(task2)
        task_repo.add(task3)

        deleted_count = task_repo.delete_by_project_id(project_id)
        assert deleted_count == 2
        assert task_repo.count() == 1  # Only task3 remains

    def test_count(self, task_repo):
        """Test counting tasks."""
        assert task_repo.count() == 0
        task1 = Task(title="Task 1", project_id=1)
        task2 = Task(title="Task 2", project_id=1)
        task_repo.add(task1)
        task_repo.add(task2)
        assert task_repo.count() == 2

    def test_exists(self, task_repo, sample_task):
        """Test checking task existence."""
        assert not task_repo.exists(sample_task.id)
        task_repo.add(sample_task)
        assert task_repo.exists(sample_task.id)

    def test_clear(self, task_repo):
        """Test clearing all tasks."""
        task1 = Task(title="Task 1", project_id=1)
        task2 = Task(title="Task 2", project_id=1)
        task_repo.add(task1)
        task_repo.add(task2)
        task_repo.clear()
        assert task_repo.count() == 0
