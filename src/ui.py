from typing import List, Tuple, Dict, Any, NamedTuple
from datetime import date
from .main_task import Task
from . import user_input


class TaskInput(NamedTuple):
    """Structured task input data."""
    name: str
    category: str
    priority: str
    deadline_str: str


class SubTaskInput(NamedTuple):
    """Structured subtask input data."""
    name: str
    deadline: date


def main_menu() -> int:
    """Display main menu and get valid user choice (1–6)."""
    while True:
        print("""
        -------------------------------------
        | STM: Smart Task Manager Console   |
        -------------------------------------
        1. Add Task
        2. View Tasks
        3. View Notifications
        4. Edit Task
        5. Delete Task
        6. Exit
        7. Mark Task as Complete
        -------------------------------------
        """)
        try:
            choice = int(input("Enter your choice (1–7): "))
            if 1 <= choice <= 7:
                return choice
            else:
                print("[!] Invalid choice. Please enter 1–7.")
        except ValueError:
            print("[!] Invalid input. Please enter a number.")


def edit_task_menu(task: Task) -> Tuple[str, str, str, date]:
    """Allow user to edit task fields (live preview of edited values)."""
    new_name, new_category, new_priority, new_deadline = (
        task.name, task.category, task.priority, task.deadline)

    while True:
        print(f"""
        ----------------------------------------
        EDIT TASK MENU - Task ID {task.task_id}
        ----------------------------------------
        1. Edit Name (current: {new_name})
        2. Edit Category (current: {new_category})
        3. Edit Priority (current: {new_priority})
        4. Edit Deadline (current: {new_deadline})
        5. Finish Editing
        """)
        choice = input("Select (1–5): ").strip()
        if choice == "1":
            new_name = user_input.read_task_name("Enter new name: ")
        elif choice == "2":
            new_category = user_input.read_category()
        elif choice == "3":
            new_priority = user_input.read_priority()
        elif choice == "4":
            new_deadline_str = user_input.read_deadline(allow_past=False, prompt="Enter new deadline (YYYY-MM-DD): ")
            y, m, d = map(int, new_deadline_str.split("-"))
            new_deadline = date(y, m, d)
        elif choice == "5":
            print("[~] Finished editing.\n")
            break
        else:
            print("[!] Invalid choice.")
    return new_name, new_category, new_priority, new_deadline


def get_task_input() -> TaskInput:
    """Collect base task details from user."""
    try:
        name = user_input.read_task_name()
        category = user_input.read_category()
        priority = user_input.read_priority()
        deadline_str = user_input.read_deadline(allow_past=False)
        return TaskInput(name, category, priority, deadline_str)
    except (ValueError, KeyboardInterrupt) as e:
        raise ValueError(f"Failed to get task input: {e}")


def get_subtask_input(parent_task: Task) -> SubTaskInput:
    """Collect subtask details with proper validation."""
    try:
        print(f"\nCreating a subtask under '{parent_task.name}' (ID {parent_task.task_id})")
        name = user_input.read_task_name("Enter subtask name: ")

        while True:
            try:
                sub_deadline_str = user_input.read_deadline(
                    allow_past=False,
                    prompt="Enter subtask deadline (YYYY-MM-DD): "
                )
                y, m, d = map(int, sub_deadline_str.split("-"))
                sub_deadline = date(y, m, d)

                if sub_deadline > parent_task.deadline:
                    print(f"[!] Subtask deadline cannot be later than parent task deadline ({parent_task.deadline}).")
                    continue
                break
            except ValueError as e:
                print(f"[!] Invalid date format: {e}")
                continue

        return SubTaskInput(name, sub_deadline)
    except (ValueError, KeyboardInterrupt) as e:
        raise ValueError(f"Failed to get subtask input: {e}")


def get_creation_options(tasks: List[Task]) -> Dict[str, Any]:
    """
    Ask whether the new entry is a SubTask or a Recurring Task and capture options.
    SubTask and Recurring are mutually exclusive. If user selects SubTask = yes,
    recurrence will be skipped.
    Returns a dict with keys:
      - is_subtask: bool
      - parent_id: int | None
      - prereq_id: int | None
      - is_recurring: bool
      - recurrence: str | None ('daily'|'weekly'|'monthly')
    """
    result: Dict[str, Any] = {
        "is_subtask": False,
        "parent_id": None,
        "prereq_id": None,
        "is_recurring": False,
        "recurrence": None,
    }

    if not tasks:
        # No parents exist, so subtask flow is impossible
        print("\n[Info] No existing tasks yet; subtask option will be skipped.")
        ask_sub = False
    else:
        ask_sub = user_input.read_yes_no("Is this a subtask of an existing task? (y/n): ")

    if ask_sub:
        # Choose parent
        print("\nExisting Tasks:")
        for t in tasks:
            print(f"  - ID {t.task_id}: {t.name} (Deadline: {t.deadline}, Status: {t.status})")
        # validate parent ID exists
        while True:
            try:
                pid_str = input("Enter parent Task ID: ").strip()
                if not pid_str.isdigit():
                    print("[!] Please enter a valid integer Task ID.")
                    continue
                pid = int(pid_str)
                if any(t.task_id == pid for t in tasks):
                    result["is_subtask"] = True
                    result["parent_id"] = pid
                    break
                print("[!] No task found with that ID. Try again.")
            except (ValueError, KeyboardInterrupt):
                print("[!] Invalid input. Please try again.")
                continue

        # Optional prerequisite subtask ID
        prereq = input("Enter prerequisite SubTask ID (press Enter if none): ").strip()
        result["prereq_id"] = int(prereq) if prereq.isdigit() else None

        # If it is a subtask, we do NOT ask for recurrence (mutually exclusive)
        return result

    # Not a subtask → ask recurrence
    is_rec = user_input.read_yes_no("Is this a recurring task? (y/n): ")
    if is_rec:
        rec = user_input.read_recurrence_type()
        result["is_recurring"] = True
        result["recurrence"] = rec

    return result


def display_tasks(tasks: List[Task]) -> None:
    """
    Display all tasks (and subtasks) in a clean, aligned table format.
    Includes recurrence info if present.
    """
    if not tasks:
        print("\n[No tasks available.]\n")
        return

    # Define uniform column widths
    col_id = 4
    col_name = 28
    col_category = 10
    col_priority = 10
    col_deadline = 14
    col_status = 10

    header = (
        f"{'ID':<{col_id}}| {'Name (Recurrence)':<{col_name}}| "
        f"{'Category':<{col_category}}| {'Priority':<{col_priority}}| "
        f"{'Deadline':<{col_deadline}}| {'Status':<{col_status}}"
    )

    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))

    for task in tasks:
        # Format recurrence neatly inside name column
        recurrence = f"[{task.recurrence}]" if hasattr(task, "recurrence") and task.recurrence else ""
        display_name = f"{task.name} {recurrence}".strip()

        print(
            f"{task.task_id:<{col_id}}| {display_name:<{col_name}}| "
            f"{task.category:<{col_category}}| {task.priority:<{col_priority}}| "
            f"{str(task.deadline):<{col_deadline}}| {task.status:<{col_status}}"
        )

        # Show subtasks under each main task (if any)
        for sub in task.subtask:
            print(
                f"   ↳ SubTask {sub.subtask_id:<2}| {sub.name:<{col_name-3}}| "
                f"{task.category:<{col_category}}| {task.priority:<{col_priority}}| "
                f"{str(sub.deadline):<{col_deadline}}| {sub.status:<{col_status}}"
            )

    print("-" * len(header) + "\n")


def display_notifications(messages: List[str]) -> None:
    """Print notification messages."""
    print("\n----------------------------------------")
    print("NOTIFICATIONS")
    print("----------------------------------------")
    if not messages:
        print("No notifications at the moment.")
    else:
        for m in messages:
            print(f"- {m}")
    print("----------------------------------------\n")
