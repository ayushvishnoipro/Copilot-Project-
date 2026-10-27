"""TodoApp business logic module.

This module defines the TodoApp class that manages task collection,
enforces business rules, and provides CRUD operations.
"""

from src.task import Task


class TodoApp:
    """Manages a collection of tasks and enforces business rules.
    
    Attributes:
        tasks (dict[int, Task]): Dictionary mapping task ID to Task object.
        next_id (int): Next sequential ID to assign to new tasks.
    """
    
    def __init__(self) -> None:
        """Initialize TodoApp with empty task collection."""
        self.tasks = {}
        self.next_id = 1
    
    def add_task(self, name: str) -> Task:
        """Add a new task to the collection.
        
        Args:
            name (str): Task description.
        
        Returns:
            Task: Newly created task.
        
        Raises:
            ValueError: If name is empty or whitespace-only.
        """
        if not self.validate_task_name(name):
            raise ValueError("Task name cannot be empty. Please enter a valid task.")
        
        task = Task(self.next_id, name.strip())
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task
    
    def get_all_tasks(self) -> list:
        """Get all tasks in creation order.
        
        Returns:
            list[Task]: List of all tasks (empty if no tasks exist).
        """
        return list(self.tasks.values())
    
    def mark_complete(self, task_id: int) -> None:
        """Mark a task as complete (idempotent).
        
        Args:
            task_id (int): ID of task to mark complete.
        
        Raises:
            KeyError: If task_id does not exist.
        """
        if not self.task_exists(task_id):
            raise KeyError(f"Task ID {task_id} not found.")
        self.tasks[task_id].mark_complete()
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task from the collection.
        
        Args:
            task_id (int): ID of task to delete.
        
        Raises:
            KeyError: If task_id does not exist.
        """
        if not self.task_exists(task_id):
            raise KeyError(f"Task ID {task_id} not found.")
        del self.tasks[task_id]
    
    def task_exists(self, task_id: int) -> bool:
        """Check if a task with given ID exists.
        
        Args:
            task_id (int): ID to check.
        
        Returns:
            bool: True if task exists, False otherwise.
        """
        return task_id in self.tasks
    
    def validate_task_name(self, name: str) -> bool:
        """Validate task name.
        
        Args:
            name (str): Task name to validate.
        
        Returns:
            bool: True if name is valid (non-empty after stripping), False otherwise.
        """
        return isinstance(name, str) and len(name.strip()) > 0
