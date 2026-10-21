"""Unit tests for the Task class."""

import pytest
from src.task import Task


class TestTask:
    """Test suite for Task class."""
    
    def test_task_initialization(self) -> None:
        """Test Task is initialized with correct id and name."""
        task = Task(1, "Buy groceries")
        assert task.id == 1
        assert task.name == "Buy groceries"
        assert task.is_complete is False
    
    def test_task_mark_complete(self) -> None:
        """Test mark_complete() sets is_complete to True."""
        task = Task(1, "Buy groceries")
        task.mark_complete()
        assert task.is_complete is True
    
    def test_task_mark_complete_idempotent(self) -> None:
        """Test mark_complete() is idempotent."""
        task = Task(1, "Buy groceries")
        task.mark_complete()
        task.mark_complete()  # Second call should not cause error
        assert task.is_complete is True
    
    def test_task_get_display_marker_incomplete(self) -> None:
        """Test get_display_marker() returns '[ ]' for incomplete task."""
        task = Task(1, "Buy groceries")
        assert task.get_display_marker() == "[ ]"
    
    def test_task_get_display_marker_complete(self) -> None:
        """Test get_display_marker() returns '[✓]' for complete task."""
        task = Task(1, "Buy groceries")
        task.mark_complete()
        assert task.get_display_marker() == "[✓]"
    
    def test_task_id_immutable(self) -> None:
        """Test Task ID is set at initialization and doesn't change."""
        task = Task(42, "Test task")
        assert task.id == 42
        # Attempt to change ID (should work in Python but not part of API)
        # This test just ensures the ID is correctly stored
    
    def test_task_name_storage(self) -> None:
        """Test Task name is stored correctly."""
        task = Task(5, "Complex task description")
        assert task.name == "Complex task description"
    
    def test_multiple_tasks_independent(self) -> None:
        """Test multiple Task instances are independent."""
        task1 = Task(1, "Task 1")
        task2 = Task(2, "Task 2")
        task1.mark_complete()
        assert task1.is_complete is True
        assert task2.is_complete is False
