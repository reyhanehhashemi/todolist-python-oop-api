"""
Main entry point for the ToDo List application.

Supports both in-memory (Phase 1) and database (Phase 2) modes.
"""

import sys

from .cli.commands import CLI
from .config import settings


def run_inmemory_mode() -> None:
    """Run application with in-memory storage (Phase 1)."""
    from .repositories.project_repository import ProjectRepository
    from .repositories.task_repository import TaskRepository
    from .services.project_service import ProjectService
    from .services.task_service import TaskService

    print("=" * 50)
    print("ToDo List Application - Phase 1 (In-Memory)")
    print("=" * 50)
    print("\nConfiguration:")
    print(f"  Max Projects: {settings.max_number_of_project}")
    print(f"  Max Tasks: {settings.max_number_of_task}")
    print()

    # Initialize repositories
    project_repo = ProjectRepository()
    task_repo = TaskRepository()

    # Initialize services
    project_service = ProjectService(project_repo, task_repo)
    task_service = TaskService(task_repo)

    # Initialize and run CLI
    cli = CLI(project_service, task_service)

    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()


def run_database_mode() -> None:
    """Run application with database storage (Phase 2)."""
    # ✅ تغییر Import - حذف get_session و اضافه get_db_context
    from .models import init_db
    from .db.session import get_db_context
    from .services.db_project_service import DBProjectService
    from .services.db_task_service import DBTaskService

    print("=" * 50)
    print("ToDo List Application - Phase 2 (Database)")
    print("=" * 50)
    print("\nConfiguration:")
    print(f"  Database URL: {settings.DATABASE_URL}")
    print(f"  Max Projects: {settings.max_number_of_project}")
    print(f"  Max Tasks: {settings.max_number_of_task}")
    print()

    # Initialize database
    try:
        print("🔧 Initializing database...")
        init_db()
        print("✅ Database initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return

    # ✅ استفاده از get_db_context به جای get_session
    try:
        with get_db_context() as session:
            # Initialize services
            project_service = DBProjectService(session)
            task_service = DBTaskService(session)

            # Initialize and run CLI
            cli = CLI(project_service, task_service)
            cli.run()

    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user.")
        # Rollback اتوماتیک توسط context manager انجام میشه
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        # Rollback اتوماتیک توسط context manager انجام میشه
        import traceback
        traceback.print_exc()
    # Close اتوماتیک توسط context manager انجام میشه
    print("\n🔒 Database session closed.")


def show_usage() -> None:
    """Display usage information."""
    print("\n📖 Usage:")
    print("  poetry run python -m todolist.main              # In-Memory mode (default)")
    print("  poetry run python -m todolist.main --db         # Database mode")
    print("  poetry run python -m todolist.main --inmemory   # In-Memory mode (explicit)")
    print("  poetry run python -m todolist.main --help       # Show this help\n")


def main() -> None:
    """
    Main entry point with mode selection.

    Defaults to in-memory mode. Use --db flag for database mode.
    """
    # Parse arguments
    mode = "inmemory"  # default

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        if arg in ["--help", "-h"]:
            show_usage()
            return
        elif arg in ["--db", "--database", "-d"]:
            mode = "database"
        elif arg in ["--inmemory", "--memory", "-m"]:
            mode = "inmemory"
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            show_usage()
            return

    # Run selected mode
    try:
        if mode == "database":
            run_database_mode()
        else:
            run_inmemory_mode()
    except Exception as e:
        print(f"\n💥 Critical error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
