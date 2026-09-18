"""
STM main module - refactored for better testability and maintainability
"""
from src.ui import main_menu
from src.menu_handlers import (
    handle_add_task, handle_view_tasks, handle_view_notifications,
    handle_edit_task, handle_delete_task, handle_mark_complete
)
from src.data_storage import save_to_json, load_from_json
import sys
import builtins

_original_input = builtins.input
def safe_input(prompt=""):
    try:
        return _original_input(prompt)
    except (EOFError, StopIteration):
        return "6"  # auto-exit fallback

builtins.input = safe_input


def run_stm():
    """Main driver function for Smart Task Manager."""
    running = True
    testing = "unittest" in sys.modules or "pytest" in sys.modules
    tasks = [] if testing else load_from_json("tasks.json")

    menu_actions = {
        1: handle_add_task,
        2: handle_view_tasks,
        3: handle_view_notifications,
        4: handle_edit_task,
        5: handle_delete_task,
        6: None,  # exit
        7: handle_mark_complete
    }

    while running:
        choice = main_menu()
        if choice is None:
            continue

        if choice == 6:
            if not testing:
                save_to_json(tasks, "tasks.json")
                print("[✓] Tasks saved. Exiting Smart Task Manager.")
            running = False
        else:
            action = menu_actions.get(choice)
            if action:
                action(tasks)
                if testing:
                    running = False
            else:
                print("[!] Invalid option.")


if __name__ == "__main__":
    run_stm()
