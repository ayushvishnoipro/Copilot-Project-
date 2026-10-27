"""Integration tests for the CLI main module."""

import pytest
from unittest.mock import patch, MagicMock
from src.main import (
    display_menu, get_user_choice, handle_add_task, handle_view_tasks,
    handle_mark_complete, handle_delete_task, run_main_loop
)
from src.todo_app import TodoApp


class TestCLI:
    """Test suite for CLI functions."""
    
    def test_display_menu_prints_options(self, capsys) -> None:
        """Test display_menu() prints menu options."""
        display_menu()
        captured = capsys.readouterr()
        assert "TO-DO APP MENU" in captured.out
        assert "1. Add Task" in captured.out
        assert "5. Exit" in captured.out
    
    def test_get_user_choice_valid_input(self) -> None:
        """Test get_user_choice() accepts valid choices."""
        with patch("builtins.input", return_value="1"):
            assert get_user_choice() == "1"
        with patch("builtins.input", return_value="5"):
            assert get_user_choice() == "5"
    
    def test_get_user_choice_invalid_input_retry(self) -> None:
        """Test get_user_choice() retries on invalid input."""
        with patch("builtins.input", side_effect=["9", "1"]):
            assert get_user_choice() == "1"
    
    def test_handle_add_task_valid_name(self, capsys) -> None:
        """Test handle_add_task() adds task and displays confirmation."""
        app = TodoApp()
        with patch("builtins.input", return_value="Buy milk"):
            handle_add_task(app)
        captured = capsys.readouterr()
        assert "Task added" in captured.out
        assert len(app.get_all_tasks()) == 1
    
    def test_handle_add_task_empty_name(self, capsys) -> None:
        """Test handle_add_task() handles empty name error."""
        app = TodoApp()
        with patch("builtins.input", return_value=""):
            handle_add_task(app)
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_handle_view_tasks_no_tasks(self, capsys) -> None:
        """Test handle_view_tasks() displays message when no tasks."""
        app = TodoApp()
        handle_view_tasks(app)
        captured = capsys.readouterr()
        assert "No tasks yet" in captured.out
    
    def test_handle_view_tasks_displays_all(self, capsys) -> None:
        """Test handle_view_tasks() displays all tasks."""
        app = TodoApp()
        app.add_task("Task 1")
        app.add_task("Task 2")
        handle_view_tasks(app)
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out
        assert "[ ]" in captured.out
    
    def test_handle_mark_complete_valid_id(self, capsys) -> None:
        """Test handle_mark_complete() marks task complete."""
        app = TodoApp()
        app.add_task("Task")
        with patch("builtins.input", return_value="1"):
            handle_mark_complete(app)
        captured = capsys.readouterr()
        assert "marked as complete" in captured.out
        assert app.tasks[1].is_complete is True
    
    def test_handle_mark_complete_invalid_id(self, capsys) -> None:
        """Test handle_mark_complete() handles invalid ID error."""
        app = TodoApp()
        with patch("builtins.input", return_value="999"):
            handle_mark_complete(app)
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    def test_handle_delete_task_valid_id(self, capsys) -> None:
        """Test handle_delete_task() deletes task."""
        app = TodoApp()
        app.add_task("Task")
        with patch("builtins.input", return_value="1"):
            handle_delete_task(app)
        captured = capsys.readouterr()
        assert "deleted" in captured.out
        assert len(app.get_all_tasks()) == 0
    
    def test_handle_delete_task_invalid_id(self, capsys) -> None:
        """Test handle_delete_task() handles invalid ID error."""
        app = TodoApp()
        with patch("builtins.input", return_value="999"):
            handle_delete_task(app)
        captured = capsys.readouterr()
        assert "Error" in captured.out


class TestMenuLoop:
    """Test suite for main loop integration."""
    
    def test_run_main_loop_exit_on_choice_5(self) -> None:
        """Test run_main_loop() exits when user chooses 5."""
        app = TodoApp()
        with patch("builtins.input", return_value="5"):
            # Should exit immediately without hanging
            run_main_loop(app)
    
    def test_run_main_loop_multiple_cycles(self) -> None:
        """Test run_main_loop() handles multiple menu cycles."""
        app = TodoApp()
        # Add task (1), view (2), mark complete (3), view (2), exit (5)
        with patch("builtins.input", side_effect=[
            "1",  # Add
            "Test task",
            "2",  # View
            "3",  # Mark complete
            "1",
            "2",  # View
            "5"   # Exit
        ]):
            run_main_loop(app)
        # After exit, app should have one completed task
        assert len(app.get_all_tasks()) == 1
        assert app.tasks[1].is_complete is True
