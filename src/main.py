"""Command-line interface for the To-Do application.

This module provides the main entry point and CLI menu loop
for user interaction with the TodoApp.
"""

from src.todo_app import TodoApp


def display_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 20)
    print("=== TO-DO APP MENU ===")
    print("=" * 20)
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Mark Task as Complete")
    print("4. Delete Task")
    print("5. Exit")
    print("=" * 20)


def get_user_choice() -> str:
    """Get and validate user menu choice.
    
    Returns:
        str: Valid user choice (1-5).
    """
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            if choice in ["1", "2", "3", "4", "5"]:
                return choice
            else:
                print("Invalid selection. Please choose a valid option (1-5).")
        except (ValueError, KeyboardInterrupt):
            print("Invalid selection. Please choose a valid option (1-5).")


def handle_add_task(app: TodoApp) -> None:
    """Handle add task menu option.
    
    Args:
        app (TodoApp): TodoApp instance.
    """
    try:
        name = input("\nEnter task name: ").strip()
        task = app.add_task(name)
        print(f"✓ Task added (ID {task.id}): {task.name}")
    except ValueError as e:
        print(f"✗ Error: {e}")


def handle_view_tasks(app: TodoApp) -> None:
    """Handle view all tasks menu option.
    
    Args:
        app (TodoApp): TodoApp instance.
    """
    tasks = app.get_all_tasks()
    if not tasks:
        print("\nNo tasks yet. Start by adding one!")
        return
    
    print("\n" + "=" * 50)
    print(f"{'ID':>3} | {'Status':^8} | Task Name")
    print("-" * 50)
    for task in tasks:
        print(f"{task.id:>3} | {task.get_display_marker():^8} | {task.name}")
    print("=" * 50)


def handle_mark_complete(app: TodoApp) -> None:
    """Handle mark task complete menu option.
    
    Args:
        app (TodoApp): TodoApp instance.
    """
    try:
        task_id_str = input("\nEnter task ID: ").strip()
        task_id = int(task_id_str)
        app.mark_complete(task_id)
        print(f"✓ Task {task_id} marked as complete.")
    except ValueError:
        print("✗ Error: Please enter a valid task ID (integer).")
    except KeyError:
        print("✗ Error: Task ID not found")


def handle_delete_task(app: TodoApp) -> None:
    """Handle delete task menu option.
    
    Args:
        app (TodoApp): TodoApp instance.
    """
    try:
        task_id_str = input("\nEnter task ID: ").strip()
        task_id = int(task_id_str)
        app.delete_task(task_id)
        print(f"✓ Task {task_id} deleted.")
    except ValueError:
        print("✗ Error: Please enter a valid task ID (integer).")
    except KeyError:
        print("✗ Error: Task ID not found")


def run_main_loop(app: TodoApp) -> None:
    """Run the main menu loop.
    
    Args:
        app (TodoApp): TodoApp instance.
    """
    while True:
        display_menu()
        choice = get_user_choice()
        
        if choice == "1":
            handle_add_task(app)
        elif choice == "2":
            handle_view_tasks(app)
        elif choice == "3":
            handle_mark_complete(app)
        elif choice == "4":
            handle_delete_task(app)
        elif choice == "5":
            print("\nGoodbye!")
            break


def main() -> None:
    """Main entry point for the To-Do application."""
    try:
        app = TodoApp()
        run_main_loop(app)
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print("Returning to menu...")


if __name__ == "__main__":
    main()
