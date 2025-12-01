"""
Unit tests for Project model.
"""

import pytest
from src.todolist.models.project import Project
from src.todolist.utils.exceptions import ValidationError


class TestProject:
    """Test Project model functionality."""

    def test_project_creation_valid(self):
        """Test creating a valid project."""
        project = Project(title="Test Project", description="Test Description")

        assert project.title == "Test Project"
        assert project.description == "Test Description"
        assert project.id is not None
        assert project.created_at is not None
        assert project.updated_at is not None

    def test_project_creation_empty_title(self):
        """Test that empty title raises validation error."""
        with pytest.raises(ValidationError, match="Project title cannot be empty"):
            Project(title="")

    def test_project_creation_title_too_many_words(self):
        """Test that title exceeding max words raises error."""
        long_title = " ".join(["word"] * 31)  # 31 words
        with pytest.raises(ValidationError, match="must not exceed 30 words"):
            Project(title=long_title)

    def test_project_creation_description_too_many_words(self):
        """Test that description exceeding max words raises error."""
        long_description = " ".join(["word"] * 151)  # 151 words
        with pytest.raises(ValidationError, match="must not exceed 150 words"):
            Project(title="Valid Title", description=long_description)

    def test_project_creation_no_description(self):
        """Test creating project without description."""
        project = Project(title="Test Project")

        assert project.title == "Test Project"
        assert project.description == ""

    def test_update_details(self):
        """Test updating project details."""
        project = Project(title="Original", description="Original desc")

        project.update_details(title="Updated", description="Updated desc")

        assert project.title == "Updated"
        assert project.description == "Updated desc"

    def test_update_details_partial(self):
        """Test updating only title."""
        project = Project(title="Original", description="Original desc")

        project.update_details(title="New Title")

        assert project.title == "New Title"
        assert project.description == "Original desc"

    def test_str_representation(self):
        """Test string representation of project."""
        project = Project(title="Test Project")
        str_repr = str(project)

        assert "Test Project" in str_repr

    def test_project_title_30_words_valid(self):
        """Test that title with exactly 30 words is valid."""
        title_30_words = " ".join(["word"] * 30)
        project = Project(title=title_30_words)
        assert project.title == title_30_words

    def test_project_description_150_words_valid(self):
        """Test that description with exactly 150 words is valid."""
        desc_150_words = " ".join(["word"] * 150)
        project = Project(title="Test", description=desc_150_words)
        assert project.description == desc_150_words

    def test_update_project_title_too_many_words(self):
        """Test updating project with title exceeding word limit."""
        project = Project(title="Valid Title")
        long_title = " ".join(["word"] * 31)

        with pytest.raises(ValidationError, match="must not exceed 30 words"):
            project.update_details(title=long_title)

    def test_update_project_description_too_many_words(self):
        """Test updating project with description exceeding word limit."""
        project = Project(title="Valid Title")
        long_desc = " ".join(["word"] * 151)

        with pytest.raises(ValidationError, match="must not exceed 150 words"):
            project.update_details(description=long_desc)
