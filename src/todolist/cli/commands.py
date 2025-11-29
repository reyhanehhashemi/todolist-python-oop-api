"""
CLI command handlers for the ToDo List application.

This module provides interactive command-line interface for
managing projects and tasks.
"""

from typing import Optional
from datetime import datetime
from ..models.task import TaskStatus
from ..services.project_service import ProjectService
from ..services.task_service import TaskService
from ..utils.exceptions import (
    ToDoListException,
    ResourceNotFoundError,
    ValidationError,
)


class CLI:
    """Command-line interface for ToDo List application."""

    def __init__(
            self, project_service: ProjectService, task_service: TaskService
    ) -> None:
        """
        Initialize CLI.

        Args:
            project_service: Service for project operations
            task_service: Service for task operations
        """
        self._project_service = project_service
        self._task_service = task_service

    def display_menu(self) -> None:
        """Display main menu."""
        print("\n" + "=" * 50)
        print("ToDo List - Main Menu")
        print("=" * 50)
        print("\nProject Management:")
        print("  1. Create Project")
        print("  2. List All Projects")
        print("  3. View Project Details")
        print("  4. Update Project")
        print("  5. Delete Project")
        print("\nTask Management:")
        print("  6. Create Task")
        print("  7. List All Tasks")
        print("  8. List Tasks by Project")
        print("  9. Update Task")
        print(" 10. Update Task Status")
        print(" 11. Delete Task")
        print("\nOther:")
        print(" 12. Show Statistics")
        print("  0. Exit")
        print("=" * 50)

    def run(self) -> None:
        """Run the CLI application."""
        print("\n🎯 Welcome to ToDo List Manager!")

        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice: ").strip()

                if choice == "0":
                    print("\n👋 Goodbye!")
                    break
                elif choice == "1":
                    self._create_project()
                elif choice == "2":
                    self._list_projects()
                elif choice == "3":
                    self._view_project_details()
                elif choice == "4":
                    self._update_project()
                elif choice == "5":
                    self._delete_project()
                elif choice == "6":
                    self._create_task()
                elif choice == "7":
                    self._list_all_tasks()
                elif choice == "8":
                    self._list_tasks_by_project()
                elif choice == "9":
                    self._update_task()
                elif choice == "10":
                    self._update_task_status()
                elif choice == "11":
                    self._delete_task()
                elif choice == "12":
                    self._show_statistics()

                else:
                    print("\n❌ Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except ToDoListException as e:
                print(f"\n❌ Error: {e}")
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}")

    def _get_integer_input(self, prompt: str) -> Optional[int]:
        """
        Get integer input from user.

        Args:
            prompt: Prompt message

        Returns:
            Integer value or None if invalid
        """
        try:
            value = input(prompt).strip()
            return int(value)
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")
            return None

    def _create_project(self) -> None:
        """Handle project creation."""
        print("\n--- Create New Project ---")
        title = input("Project Title (max 30 words): ").strip()
        description = input("Description (optional, max 150 words): ").strip()

        try:
            project = self._project_service.create_project(title, description)
            print(f"\n✅ Project created successfully!")
            print(f"   ID: {project.id}")
            print(f"   Title: {project.title}")
        except ToDoListException as e:
            print(f"\n❌ Failed to create project: {e}")

    def _list_projects(self) -> None:
        """Handle listing all projects."""
        print("\n--- All Projects ---")
        projects = self._project_service.get_all_projects()

        if not projects:
            print("No projects found.")
            return

        for idx, project in enumerate(projects, 1):
            print(f"\n{idx}. {project.title}")
            print(f"   ID: {project.id}")
            print(f"   Description: {project.description or '(no description)'}")
            print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")

    def _view_project_details(self) -> None:
        """Handle viewing project details with tasks."""
        print("\n--- View Project Details ---")
        project_id = self._get_integer_input("Enter Project ID: ")

        if project_id is None:
            return

        try:
            summary = self._project_service.get_project_summary(project_id)
            project = summary["project"]

            print(f"\n📁 Project: {project.title}")
            print(f"   ID: {project.id}")
            print(f"   Description: {project.description or '(no description)'}")
            print(f"   Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"\n📊 Task Statistics:")
            print(f"   Total Tasks: {summary['total_tasks']}")
            for status, count in summary["status_breakdown"].items():
                print(f"   {status}: {count}")

            # List tasks
            tasks = self._task_service.get_tasks_by_project(project_id)
            if tasks:
                print(f"\n📝 Tasks:")
                for idx, task in enumerate(tasks, 1):
                    deadline_str = f" | 📅 {task.deadline.strftime('%Y-%m-%d %H:%M')}" if task.deadline else ""
                    print(f"   {idx}. [{task.status}] {task.title}{deadline_str}")
                    print(f"      ID: {task.id}")

        except ResourceNotFoundError as e:
            print(f"\n❌ {e}")

    def _update_project(self) -> None:
        """Handle project update."""
        print("\n--- Update Project ---")
        project_id = self._get_integer_input("Enter Project ID: ")

        if project_id is None:
            return

        try:
            project = self._project_service.get_project(project_id)
            print(f"\nCurrent Title: {project.title}")
            print(f"Current Description: {project.description or '(empty)'}")

            new_title = input("\nNew Title (max 30 words, press Enter to keep current): ").strip()
            new_description = input("New Description (max 150 words, press Enter to keep current): ").strip()

            updated_project = self._project_service.update_project(
                project_id,
                title=new_title if new_title else None,
                description=new_description if new_description else None,
            )

            print(f"\n✅ Project updated successfully!")
            print(f"   Title: {updated_project.title}")
            print(f"   Description: {updated_project.description}")

        except ToDoListException as e:
            print(f"\n❌ {e}")

    def _delete_project(self) -> None:
        """Handle project deletion."""
        print("\n--- Delete Project ---")
        project_id = self._get_integer_input("Enter Project ID: ")

        if project_id is None:
            return

        try:
            project = self._project_service.get_project(project_id)
            print(f"\n⚠️  You are about to delete: {project.title}")

            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Deletion cancelled.")
                return

            result = self._project_service.delete_project(project_id)
            print(f"\n✅ Project deleted successfully!")
            print(f"   Deleted {result['deleted_tasks']} associated tasks.")

        except ResourceNotFoundError as e:
            print(f"\n❌ {e}")

    def _create_task(self) -> None:
        """Handle task creation."""
        print("\n--- Create New Task ---")

        # Show available projects
        projects = self._project_service.get_all_projects()
        if not projects:
            print("❌ No projects available. Please create a project first.")
            return

        print("\nAvailable Projects:")
        for idx, project in enumerate(projects, 1):
            print(f"  {idx}. {project.title} (ID: {project.id})")

        project_id = self._get_integer_input("\nEnter Project ID: ")

        if project_id is None:
            return

        title = input("Task Title (max 30 words): ").strip()
        description = input("Description (optional, max 150 words): ").strip()

        # Get deadline
        deadline = None
        deadline_input = input("Deadline (YYYY-MM-DD HH:MM) (optional, press Enter to skip): ").strip()

        if deadline_input:
            try:
                deadline = datetime.strptime(deadline_input, "%Y-%m-%d %H:%M")
            except ValueError:
                print("❌ Invalid date format. Please use YYYY-MM-DD HH:MM format (e.g., 2025-10-20 14:30).")
                return

        try:
            task = self._task_service.create_task(
                title,
                project_id,
                description,
                deadline=deadline
            )
            print(f"\n✅ Task created successfully!")
            print(f"   ID: {task.id}")
            print(f"   Title: {task.title}")
            print(f"   Status: {task.status}")
            if task.deadline:
                print(f"   Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}")

        except ToDoListException as e:
            print(f"\n❌ Failed to create task: {e}")

    def _list_all_tasks(self) -> None:
        """Handle listing all tasks."""
        print("\n--- All Tasks ---")
        tasks = self._task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for idx, task in enumerate(tasks, 1):
            deadline_str = f" | 📅 Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}" if task.deadline else ""
            print(f"\n{idx}. [{task.status}] {task.title}{deadline_str}")
            print(f"   ID: {task.id}")
            print(f"   Project ID: {task.project_id}")
            print(f"   Description: {task.description or '(no description)'}")

    def _list_tasks_by_project(self) -> None:
        """Handle listing tasks for a specific project."""
        print("\n--- Tasks by Project ---")
        project_id = self._get_integer_input("Enter Project ID: ")

        if project_id is None:
            return

        try:
            project = self._project_service.get_project(project_id)
            tasks = self._task_service.get_tasks_by_project(project_id)

            print(f"\n📁 Project: {project.title}")
            print(f"📝 Tasks ({len(tasks)}):")

            if not tasks:
                print("   No tasks in this project.")
                return

            for idx, task in enumerate(tasks, 1):
                deadline_str = f" | 📅 {task.deadline.strftime('%Y-%m-%d %H:%M')}" if task.deadline else ""
                print(f"\n{idx}. [{task.status}] {task.title}{deadline_str}")
                print(f"   ID: {task.id}")
                print(f"   Description: {task.description or '(no description)'}")

        except ResourceNotFoundError as e:
            print(f"\n❌ {e}")

    def _update_task(self) -> None:
        """Handle task update."""
        print("\n--- Update Task ---")
        task_id = self._get_integer_input("Enter Task ID: ")

        if task_id is None:
            return

        try:
            task = self._task_service.get_task(task_id)
            print(f"\nCurrent Title: {task.title}")
            print(f"Current Description: {task.description or '(empty)'}")
            print(f"Current Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M') if task.deadline else '(not set)'}")

            new_title = input("\nNew Title (max 30 words, press Enter to keep current): ").strip()
            new_description = input("New Description (max 150 words, press Enter to keep current): ").strip()

            new_deadline = None
            deadline_input = input("New Deadline (YYYY-MM-DD HH:MM) (press Enter to keep current): ").strip()

            if deadline_input:
                try:
                    new_deadline = datetime.strptime(deadline_input, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("❌ Invalid date format. Please use YYYY-MM-DD HH:MM format. Update cancelled.")
                    return

            updated_task = self._task_service.update_task(
                task_id,
                title=new_title if new_title else None,
                description=new_description if new_description else None,
                deadline=new_deadline if deadline_input else None,
            )

            print(f"\n✅ Task updated successfully!")
            print(f"   Title: {updated_task.title}")
            print(f"   Description: {updated_task.description}")
            if updated_task.deadline:
                print(f"   Deadline: {updated_task.deadline.strftime('%Y-%m-%d %H:%M')}")

        except ToDoListException as e:
            print(f"\n❌ {e}")

    def _update_task_status(self) -> None:
        """Handle task status update."""
        print("\n--- Update Task Status ---")
        task_id = self._get_integer_input("Enter Task ID: ")

        if task_id is None:
            return

        try:
            task = self._task_service.get_task(task_id)
            print(f"\nCurrent Status: {task.status}")
            print("\nAvailable Statuses:")
            for idx, status in enumerate(TaskStatus.values(), 1):
                print(f"  {idx}. {status}")

            new_status = input("\nEnter new status: ").strip().upper()

            updated_task = self._task_service.update_task_status(task_id, new_status)
            print(f"\n✅ Task status updated to: {updated_task.status}")

        except ToDoListException as e:
            print(f"\n❌ {e}")

    def _delete_task(self) -> None:
        """Handle task deletion."""
        print("\n--- Delete Task ---")
        task_id = self._get_integer_input("Enter Task ID: ")

        if task_id is None:
            return

        try:
            task = self._task_service.get_task(task_id)
            print(f"\n⚠️  You are about to delete: {task.title}")

            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Deletion cancelled.")
                return

            self._task_service.delete_task(task_id)
            print(f"\n✅ Task deleted successfully!")

        except ResourceNotFoundError as e:
            print(f"\n❌ {e}")

    def _show_statistics(self) -> None:
        """Display application statistics."""
        print("\n--- Statistics ---")

        total_projects = self._project_service.count_projects()
        total_tasks = self._task_service.count_tasks()

        print(f"\n📊 Overview:")
        print(f"   Total Projects: {total_projects}")
        print(f"   Total Tasks: {total_tasks}")

        # Task breakdown by status
        print(f"\n📝 Tasks by Status:")
        for status in TaskStatus.values():
            count = len(self._task_service.get_tasks_by_status(status))
            print(f"   {status}: {count}")


