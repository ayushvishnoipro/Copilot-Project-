"""Task data model module.

This module defines the Task class that encapsulates a single task
with immutable ID and mutable completion status.
"""


class Task:
    """Represents a single task in the to-do application.
    
    Attributes:
        id (int): Auto-assigned sequential task ID (immutable).
        name (str): Task description/name.
        is_complete (bool): Task completion status (default False).
    """
    
    def __init__(self, id: int, name: str) -> None:
        """Initialize a Task with given ID and name.
        
        Args:
            id (int): Sequential task ID.
            name (str): Task description.
        """
        self.id = id
        self.name = name
        self.is_complete = False
    
    def mark_complete(self) -> None:
        """Mark this task as complete (idempotent)."""
        self.is_complete = True
    
    def get_display_marker(self) -> str:
        """Return display marker based on completion status.
        
        Returns:
            str: "[✓]" if complete, "[ ]" if incomplete.
        """
        return "[✓]" if self.is_complete else "[ ]"
