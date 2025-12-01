# tests/integration/test_end_to_end.py

import pytest
from datetime import datetime, timedelta
from src.todolist.models.task import TaskStatus
from src.todolist.services.project_service import ProjectService
from src.todolist.services.task_service import TaskService
from src.todolist.repositories.project_repository import ProjectRepository
from src.todolist.repositories.task_repository import TaskRepository
from src.todolist.utils.exceptions import ResourceNotFoundError  # ✅ اضافه شد


class TestEndToEnd:
    """Integration tests for complete workflows."""

    @pytest.fixture
    def setup_services(self):
        """Setup services for testing."""
        project_repo = ProjectRepository()
        task_repo = TaskRepository()
        project_service = ProjectService(project_repo, task_repo)
        task_service = TaskService(task_repo)
        return project_service, task_service

    def test_complete_workflow(self, setup_services):
        """Test complete user workflow from project creation to deletion."""
        project_service, task_service = setup_services

        # 1. Create project
        project = project_service.create_project(
            "My Project", "Test project description"
        )
        assert project.title == "My Project"

        # 2. Create tasks
        task1 = task_service.create_task("Task 1", project.id, "First task")
        task2 = task_service.create_task("Task 2", project.id, "Second task")

        # 3. Verify tasks in project
        tasks = task_service.get_tasks_by_project(project.id)
        assert len(tasks) == 2

        # 4. Update task status
        task_service.update_task_status(task1.id, TaskStatus.DOING.value)

        # 5. Verify status update
        updated_task = task_service.get_task(task1.id)
        assert updated_task.status == TaskStatus.DOING.value

        # 6. Complete task
        task_service.update_task_status(task1.id, TaskStatus.DONE.value)
        completed_task = task_service.get_task(task1.id)
        assert completed_task.status == TaskStatus.DONE.value

        # 7. Get tasks by status
        doing_tasks = task_service.get_tasks_by_status(TaskStatus.DOING.value)
        assert len(doing_tasks) == 0

        done_tasks = task_service.get_tasks_by_status(TaskStatus.DONE.value)
        assert len(done_tasks) == 1

        # 8. Delete project (cascading delete)
        project_service.delete_project(project.id)
        with pytest.raises(ResourceNotFoundError):  # ✅ تغییر از ValueError
            project_service.get_project(project.id)

        # Verify tasks are also deleted
        tasks = task_service.get_tasks_by_project(project.id)
        assert len(tasks) == 0

    def test_multiple_projects_workflow(self, setup_services):
        """Test workflow with multiple projects."""
        project_service, task_service = setup_services

        # Create two projects
        project1 = project_service.create_project("Project 1", "First project")
        project2 = project_service.create_project("Project 2", "Second project")

        # Create tasks for each project
        task1 = task_service.create_task("Task 1", project1.id, "Task for project 1")
        task2 = task_service.create_task("Task 2", project2.id, "Task for project 2")

        # Verify tasks are assigned correctly
        p1_tasks = task_service.get_tasks_by_project(project1.id)
        p2_tasks = task_service.get_tasks_by_project(project2.id)

        assert len(p1_tasks) == 1
        assert len(p2_tasks) == 1
        assert p1_tasks[0].project_id == project1.id
        assert p2_tasks[0].project_id == project2.id

        # Delete one project
        project_service.delete_project(project1.id)

        # Verify only project1 tasks are deleted
        p1_tasks = task_service.get_tasks_by_project(project1.id)
        p2_tasks = task_service.get_tasks_by_project(project2.id)

        assert len(p1_tasks) == 0
        assert len(p2_tasks) == 1
