"""
Menu handler functions for STM - separated for better testability
"""
from datetime import date
from src.ui import get_task_input, get_subtask_input, display_tasks, display_notifications, edit_task_menu
from src.main_task import add_task, delete_task, edit_task
from src.notification import notify_upcoming_deadlines, notify_overdue_tasks
from src.analytics import get_summary, calculate_completion_rate, get_category_summary
from src.sub_task import SubTask
from src import user_input
from rich.console import Console
from rich.table import Table
console = Console()



def handle_add_task(tasks):
    """Handle add task menu option"""
    while True:
        task_type = input("Create a Main Task or SubTask? (m/s): ").strip().lower()
        if task_type in ("m", "s"):
            break
        print("[!] Invalid choice. Please enter 'm' for main or 's' for subtask.\n")

    if task_type == "m":
        return handle_add_main_task(tasks)
    else:
        return handle_add_subtask(tasks)


def handle_add_main_task(tasks):
    """Handle adding a main task"""
    while True:
        try:
            name, category, priority, deadline_str = get_task_input()
            y, m, d = map(int, deadline_str.split("-"))
            deadline = date(y, m, d)
            if deadline < date.today():
                print("[!] Deadline cannot be in the past.\n")
                continue
            break
        except ValueError:
            print("[!] Invalid date format. Please try again.\n")

    is_recurring = user_input.read_yes_no("Is this a recurring task? (y/n): ")
    recurrence_type = None
    if is_recurring:
        print("\nSelect Recurrence Type:")
        print("1. Daily\n2. Weekly\n3. Monthly")
        rec_choice = user_input.read_integer_range("Enter your choice (1–3): ", 1, 3)
        recurrence_type = (
            "daily" if rec_choice == 1
            else "weekly" if rec_choice == 2
            else "monthly"
        )

    new_task = add_task(name, category, priority, deadline)
    new_task.recurrence = recurrence_type
    tasks.append(new_task)
    print(f"[+] Task '{name}' added successfully! Recurrence: {recurrence_type or 'none'}\n")
    return True


def handle_add_subtask(tasks):
    """Handle adding a subtask"""
    if not tasks:
        print("[!] No main tasks available. Please create one first.")
        return False

    print("\nAvailable Main Tasks:")
    for t in tasks:
        print(f"  {t.task_id}. {t.name} (Deadline: {t.deadline})")

    parent_task = get_valid_parent_task(tasks)
    if not parent_task:
        return False

    while True:
        sub_name, sub_deadline = get_subtask_input(parent_task)
        if sub_deadline > parent_task.deadline:
            print(f"[!] SubTask deadline cannot exceed parent task's deadline ({parent_task.deadline}).\n")
            continue
        break

    next_sub_id = 1 + max((s.subtask_id for s in parent_task.subtask), default=0)
    sub = SubTask(
        subtask_id=next_sub_id,
        parent_task_id=parent_task.task_id,
        name=sub_name,
        priority=parent_task.priority,
        deadline=sub_deadline,
    )

    parent_task.add_subtask(sub)
    print(f"[+] SubTask '{sub_name}' added under '{parent_task.name}'.\n")
    return True


def get_valid_parent_task(tasks):
    """Get a valid parent task from user input"""
    while True:
        parent_id_input = input("Enter parent Task ID: ").strip()
        if not parent_id_input.isdigit():
            print("[!] Invalid input. Please enter a valid numeric Task ID.\n")
            continue
        parent_id = int(parent_id_input)
        parent_task = next((t for t in tasks if t.task_id == parent_id), None)
        if not parent_task:
            print("[!] Parent task not found. Please enter a valid Task ID.\n")
            continue
        return parent_task


def handle_view_tasks(tasks):
    """Handle view tasks menu option"""
    if not tasks:
        print("\n[No tasks available to display.]\n")
        return

    display_tasks(tasks)
    display_analytics(tasks)


def display_analytics(tasks):
    """Display analytics in a Rich-formatted table."""
    summary = get_summary(tasks)
    completion_rate = calculate_completion_rate(tasks)
    category_summary = get_category_summary(tasks)

    # Main summary table
    table = Table(title="Task Summary Overview", show_lines=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right", style="green")

    table.add_row("Total Tasks", str(summary["total"]))
    table.add_row("Completed", str(summary["completed"]))
    table.add_row("Pending", str(summary["pending"]))
    table.add_row("Overdue", str(summary["overdue"]))
    table.add_row("Completion Rate (%)", f"{completion_rate:.2f}")

    console.print(table)

    # Category summary table
    if category_summary:
        cat_table = Table(title="Tasks by Category", show_lines=True)
        cat_table.add_column("Category", style="magenta")
        cat_table.add_column("Count", justify="right", style="yellow")
        for cat, count in category_summary.items():
            cat_table.add_row(cat, str(count))
        console.print(cat_table)
    else:
        console.print("[yellow]No categories to display.[/yellow]")


def handle_view_notifications(tasks):
    """Handle view notifications menu option"""
    today = date.today()
    notifications = notify_upcoming_deadlines(tasks, today) + notify_overdue_tasks(tasks, today)
    display_notifications(notifications)


def handle_edit_task(tasks):
    """Handle edit task menu option"""
    if not tasks:
        print("[!] No tasks available to edit.\n")
        return

    while True:
        edit_type = input("Edit a Main Task or SubTask? (m/s): ").strip().lower()
        if edit_type in ("m", "s"):
            break
        print("[!] Invalid choice. Please enter 'm' for main or 's' for subtask.\n")

    if edit_type == "m":
        return handle_edit_main_task(tasks)
    else:
        return handle_edit_subtask(tasks)


def handle_edit_main_task(tasks):
    """Handle editing a main task"""
    print("\nAvailable Main Tasks:")
    display_tasks(tasks)

    task = get_valid_task_by_id(tasks, "Enter Main Task ID to edit (or 'c' to cancel): ")
    if not task:
        return

    new_name, new_cat, new_prio, new_dead = edit_task_menu(task)
    if new_dead < date.today():
        print("[!] Deadline cannot be in the past.")
        return

    edit_task(task, new_name, new_cat, new_prio, new_dead)
    print(f"[~] Main Task '{task.name}' updated successfully!\n")


def handle_edit_subtask(tasks):
    """Handle editing a subtask - simplified version"""
    has_subtasks = any(t.subtask for t in tasks)
    if not has_subtasks:
        print("[!] No subtasks available to edit.\n")
        return

    print("[~] Subtask editing not implemented in this simplified version.\n")


def get_valid_task_by_id(tasks, prompt):
    """Get a valid task by ID with cancellation option"""
    while True:
        task_id_input = input(prompt).strip()
        if task_id_input.lower() == "c":
            print("[~] Operation cancelled.\n")
            return None
        if not task_id_input.isdigit():
            print("[!] Invalid input. Please enter a numeric Task ID.\n")
            continue
        task_id = int(task_id_input)
        task = next((t for t in tasks if t.task_id == task_id), None)
        if not task:
            print("[!] Task not found. Please enter a valid Task ID.\n")
            continue
        return task


def handle_delete_task(tasks):
    """Handle delete task menu option"""
    if not tasks:
        print("[!] No tasks available to delete.\n")
        return

    while True:
        delete_type = input("Delete a Main Task or SubTask? (m/s): ").strip().lower()
        if delete_type in ("m", "s"):
            break
        print("[!] Invalid choice. Please enter 'm' for main or 's' for subtask.\n")

    if delete_type == "m":
        return handle_delete_main_task(tasks)
    else:
        return handle_delete_subtask(tasks)



def handle_delete_main_task(tasks):
    """Handle deleting a main task"""
    display_tasks(tasks)
    task = get_valid_task_by_id(tasks, "Enter Main Task ID to delete (or 'c' to cancel): ")
    if not task:
        return

    confirm = user_input.read_yes_no(
        f"Are you sure you want to delete '{task.name}' and its subtasks? (y/n): "
    )
    if confirm:
        tasks.remove(task)
        print(f"[-] Main Task '{task.name}' (and all its subtasks) deleted.\n")
    else:
        print("[~] Deletion cancelled.\n")

def handle_delete_subtask(tasks):
    """Handle deleting a subtask under a specific main task"""
    has_subtasks = any(t.subtask for t in tasks)
    if not has_subtasks:
        print("[!] No subtasks available to delete.\n")
        return False

    # Display all subtasks grouped by parent
    print("\nAvailable SubTasks:")
    for t in tasks:
        if t.subtask:
            print(f"\nParent Task: {t.name} (ID {t.task_id})")
            for s in t.subtask:
                print(f"   ↳ SubTask {s.subtask_id}: {s.name} (Deadline: {s.deadline}, Status: {s.status})")

    # Ask for parent and subtask IDs
    try:
        parent_id = int(input("\nEnter the Parent Task ID: ").strip())
        parent_task = next((t for t in tasks if t.task_id == parent_id), None)
        if not parent_task:
            print("[!] Parent task not found.\n")
            return False

        if not parent_task.subtask:
            print("[!] This parent task has no subtasks.\n")
            return False

        sub_id = int(input("Enter the SubTask ID to delete: ").strip())
        sub_to_delete = next((s for s in parent_task.subtask if s.subtask_id == sub_id), None)
        if not sub_to_delete:
            print("[!] No subtask found with that ID.\n")
            return False

        confirm = user_input.read_yes_no(
            f"Are you sure you want to delete SubTask '{sub_to_delete.name}'? (y/n): "
        )
        if confirm:
            parent_task.subtask.remove(sub_to_delete)
            print(f"[-] SubTask '{sub_to_delete.name}' deleted successfully.\n")
            return True
        else:
            print("[~] Deletion cancelled.\n")
            return False
    except ValueError:
        print("[!] Invalid input. Please enter numeric IDs.\n")
        return False



def handle_mark_complete(tasks):
    """Handle mark task complete menu option"""
    if not tasks:
        print("[!] No tasks available.\n")
        return

    while True:
        mark_type = input("Mark a Main Task or SubTask? (m/s): ").strip().lower()
        if mark_type in ("m", "s"):
            break
        print("[!] Invalid choice. Please enter 'm' for main or 's' for subtask.\n")

    if mark_type == "m":
        return handle_mark_main_task_complete(tasks)
    else:
        print("[~] SubTask completion not implemented in this simplified version.\n")


def handle_mark_main_task_complete(tasks):
    """Handle marking a main task as complete"""
    display_tasks(tasks)
    task = get_valid_task_by_id(tasks, "Enter Task ID to mark complete (or 'c' to cancel): ")
    if not task:
        return

    if not task.mark_complete():
        print("[!] Cannot mark as complete — some subtasks are still pending.\n")
    else:
        print(f"[✓] Task '{task.name}' marked as completed!\n")
