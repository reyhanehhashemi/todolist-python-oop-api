"""
Unit tests for Task model.
"""

import pytest
from datetime import datetime, timedelta
from src.todolist.models.task import Task, TaskStatus
from src.todolist.utils.exceptions import ValidationError


class TestTask:
    """Test suite for Task model."""

    def test_task_creation_valid(self):
        """Test valid task creation."""
        task = Task(
            title="Test Task",
            description="Test description",
            project_id=1
        )
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.project_id == 1
        assert task.status == TaskStatus.TODO.value
        assert task.id > 0
        assert task.deadline is None

    def test_task_creation_empty_title(self):
        """Test task creation with empty title raises error."""
        with pytest.raises(ValidationError, match="cannot be empty"):
            Task(title="", description="Test", project_id=1)

    def test_task_creation_title_too_many_words(self):
        """Test task creation with too many words in title raises error."""
        long_title = " ".join(["word"] * 31)  # 31 words
        with pytest.raises(ValidationError, match="must not exceed 30 words"):
            Task(title=long_title, description="Test", project_id=1)

    def test_task_description_too_many_words(self):
        """Test task description exceeding 150 words raises error."""
        long_desc = " ".join(["word"] * 151)  # 151 words
        with pytest.raises(ValidationError, match="must not exceed 150 words"):
            Task(title="Valid title", description=long_desc, project_id=1)

    def test_task_creation_invalid_status(self):
        """Test task creation with invalid status raises error."""
        with pytest.raises(ValidationError, match="must be one of"):
            Task(title="Test", description="Test", project_id=1, status="INVALID")

    def test_update_status_valid(self):
        """Test updating task status to valid value."""
        task = Task(title="Test", description="Test", project_id=1)
        task.update_status(TaskStatus.DOING.value)
        assert task.status == TaskStatus.DOING.value

    def test_update_status_invalid(self):
        """Test updating task status to invalid value raises error."""
        task = Task(title="Test", description="Test", project_id=1)
        with pytest.raises(ValidationError, match="must be one of"):
            task.update_status("INVALID_STATUS")

    def test_update_details(self):
        """Test updating task details."""
        task = Task(title="Original", description="Original desc", project_id=1)
        task.update_details(title="Updated", description="Updated desc")
        assert task.title == "Updated"
        assert task.description == "Updated desc"

    def test_update_details_partial(self):
        """Test updating only some task details."""
        task = Task(title="Original", description="Original desc", project_id=1)
        task.update_details(title="Updated")
        assert task.title == "Updated"
        assert task.description == "Original desc"

    def test_str_representation(self):
        """Test string representation of task."""
        task = Task(title="Test Task", description="Test desc", project_id=1)
        task_str = str(task)
        assert "Test Task" in task_str
        assert "TODO" in task_str

    # Deadline tests
    def test_task_creation_with_valid_deadline(self):
        """Test task creation with valid future deadline."""
        future_deadline = datetime.now() + timedelta(days=7)
        task = Task(
            title="Test Task",
            description="Test description",
            project_id=1,
            deadline=future_deadline
        )
        assert task.deadline == future_deadline

    def test_task_creation_with_past_deadline(self):
        """Test task creation with past deadline raises error."""
        past_deadline = datetime.now() - timedelta(days=1)
        with pytest.raises(ValidationError, match="cannot be in the past"):
            Task(
                title="Test Task",
                description="Test description",
                project_id=1,
                deadline=past_deadline
            )

    def test_task_creation_without_deadline(self):
        """Test task creation without deadline is valid."""
        task = Task(
            title="Test Task",
            description="Test description",
            project_id=1
        )
        assert task.deadline is None

    def test_update_task_deadline(self):
        """Test updating task deadline."""
        task = Task(title="Test", description="Test", project_id=1)
        future_deadline = datetime.now() + timedelta(days=5)

        task.update_details(deadline=future_deadline)
        assert task.deadline == future_deadline

    def test_update_task_with_past_deadline(self):
        """Test updating task with past deadline raises error."""
        task = Task(title="Test", description="Test", project_id=1)
        past_deadline = datetime.now() - timedelta(hours=1)

        with pytest.raises(ValidationError, match="cannot be in the past"):
            task.update_details(deadline=past_deadline)

    def test_task_str_with_deadline(self):
        """Test string representation includes deadline."""
        future_deadline = datetime.now() + timedelta(days=3)
        task = Task(
            title="Test Task",
            description="Test",
            project_id=1,
            deadline=future_deadline
        )
        task_str = str(task)
        assert "deadline=" in task_str

    def test_task_title_30_words_valid(self):
        """Test that title with exactly 30 words is valid."""
        title_30_words = " ".join(["word"] * 30)
        task = Task(title=title_30_words, project_id=1)
        assert task.title == title_30_words

    def test_task_description_150_words_valid(self):
        """Test that description with exactly 150 words is valid."""
        desc_150_words = " ".join(["word"] * 150)
        task = Task(title="Test", description=desc_150_words, project_id=1)
        assert task.description == desc_150_words

    def test_update_task_title_too_many_words(self):
        """Test updating task with title exceeding word limit."""
        task = Task(title="Valid Title", project_id=1)
        long_title = " ".join(["word"] * 31)

        with pytest.raises(ValidationError, match="must not exceed 30 words"):
            task.update_details(title=long_title)

    def test_update_task_description_too_many_words(self):
        """Test updating task with description exceeding word limit."""
        task = Task(title="Valid Title", project_id=1)
        long_desc = " ".join(["word"] * 151)

        with pytest.raises(ValidationError, match="must not exceed 150 words"):
            task.update_details(description=long_desc)
