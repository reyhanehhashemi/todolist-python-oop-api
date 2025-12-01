"""
Auto-close overdue tasks command.
"""

import sys
import logging
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(src_dir))


def setup_logging():
    """Configure logging to both console and file."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "auto_close.log"
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '| [%(asctime)s] %(message)s |',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def auto_close_overdue_tasks():
    """Close all tasks that have passed their deadline."""
    logger = setup_logging()

    try:
        # ✅ استفاده از get_db_context از session.py
        from ..db.session import get_db_context
        from ..services.db_task_service import DBTaskService

        with get_db_context() as session:
            task_service = DBTaskService(session)
            closed_count = task_service.auto_close_overdue_tasks()
            logger.info(f"Auto-close completed: {closed_count} task(s) closed")
            return closed_count

    except Exception as e:
        error_msg = f"ERROR: {str(e)}"
        logger.error(error_msg)
        raise


def main():
    """Entry point for command-line execution."""
    try:
        closed_count = auto_close_overdue_tasks()
        sys.exit(0)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
