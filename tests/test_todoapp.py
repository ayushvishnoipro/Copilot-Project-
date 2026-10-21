"""Unit tests for the TodoApp class."""

import pytest
from src.todo_app import TodoApp
from src.task import Task


class TestTodoApp:
    """Test suite for TodoApp class."""
    
    def setup_method(self) -> None:
        """Set up a fresh TodoApp instance for each test."""
        self.app = TodoApp()
    
    def test_todoapp_initialization(self) -> None:
        """Test TodoApp initializes with empty tasks and next_id=1."""
        assert self.app.tasks == {}
        assert self.app.next_id == 1
    
    def test_add_task_valid_name(self) -> None:
        """Test add_task() with valid name creates task."""
        task = self.app.add_task("Buy groceries")
        assert task.id == 1
        assert task.name == "Buy groceries"
        assert task in self.app.tasks.values()
        assert self.app.next_id == 2
    
    def test_add_task_empty_name_raises_error(self) -> None:
        """Test add_task() with empty name raises ValueError."""
        with pytest.raises(ValueError):
            self.app.add_task("")
    
    def test_add_task_whitespace_only_raises_error(self) -> None:
        """Test add_task() with whitespace-only name raises ValueError."""
        with pytest.raises(ValueError):
            self.app.add_task("   ")
        with pytest.raises(ValueError):
            self.app.add_task("\t\n")
    
    def test_add_task_whitespace_trimmed(self) -> None:
        """Test add_task() trims leading/trailing whitespace."""
        task = self.app.add_task("  Buy groceries  ")
        assert task.name == "Buy groceries"
    
    def test_sequential_id_assignment(self) -> None:
        """Test tasks are assigned sequential IDs."""
        task1 = self.app.add_task("Task 1")
        task2 = self.app.add_task("Task 2")
        task3 = self.app.add_task("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3
        assert self.app.next_id == 4
    
    def test_get_all_tasks_empty(self) -> None:
        """Test get_all_tasks() returns empty list when no tasks."""
        assert self.app.get_all_tasks() == []
    
    def test_get_all_tasks_returns_all_in_order(self) -> None:
        """Test get_all_tasks() returns all tasks in creation order."""
        self.app.add_task("Task 1")
        self.app.add_task("Task 2")
        self.app.add_task("Task 3")
        tasks = self.app.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].name == "Task 1"
        assert tasks[1].name == "Task 2"
        assert tasks[2].name == "Task 3"
    
    def test_mark_complete_valid_id(self) -> None:
        """Test mark_complete() with valid ID marks task complete."""
        self.app.add_task("Task")
        self.app.mark_complete(1)
        assert self.app.tasks[1].is_complete is True
    
    def test_mark_complete_idempotent(self) -> None:
        """Test mark_complete() is idempotent (calling twice is safe)."""
        self.app.add_task("Task")
        self.app.mark_complete(1)
        self.app.mark_complete(1)  # Should not raise error
        assert self.app.tasks[1].is_complete is True
    
    def test_mark_complete_invalid_id_raises_error(self) -> None:
        """Test mark_complete() with invalid ID raises KeyError."""
        with pytest.raises(KeyError):
            self.app.mark_complete(999)
    
    def test_delete_task_valid_id(self) -> None:
        """Test delete_task() removes task from collection."""
        self.app.add_task("Task 1")
        self.app.add_task("Task 2")
        self.app.delete_task(1)
        assert 1 not in self.app.tasks
        assert 2 in self.app.tasks
    
    def test_delete_task_invalid_id_raises_error(self) -> None:
        """Test delete_task() with invalid ID raises KeyError."""
        with pytest.raises(KeyError):
            self.app.delete_task(999)
    
    def test_delete_task_no_renumbering(self) -> None:
        """Test IDs are not renumbered after deletion."""
        self.app.add_task("Task 1")
        self.app.add_task("Task 2")
        self.app.add_task("Task 3")
        self.app.delete_task(2)
        new_task = self.app.add_task("Task 4")
        assert new_task.id == 4  # Not 3
        assert self.app.tasks.keys() == {1, 3, 4}
    
    def test_task_exists_returns_true_for_existing(self) -> None:
        """Test task_exists() returns True for existing task."""
        self.app.add_task("Task")
        assert self.app.task_exists(1) is True
    
    def test_task_exists_returns_false_for_nonexistent(self) -> None:
        """Test task_exists() returns False for non-existing task."""
        assert self.app.task_exists(999) is False
    
    def test_validate_task_name_valid(self) -> None:
        """Test validate_task_name() accepts valid names."""
        assert self.app.validate_task_name("Valid name") is True
        assert self.app.validate_task_name("  Valid with spaces  ") is True
    
    def test_validate_task_name_invalid(self) -> None:
        """Test validate_task_name() rejects invalid names."""
        assert self.app.validate_task_name("") is False
        assert self.app.validate_task_name("   ") is False
        assert self.app.validate_task_name("\t") is False
