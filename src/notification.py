from datetime import date
from typing import List
from .main_task import Task


def notify_upcoming_deadlines(tasks: List[Task], current_date: date) -> List[str]:
    """Notify of tasks due within 3 days."""
    notifications = []
    for task in tasks:
        if task.status.lower() != "completed":
            days_remaining = (task.deadline - current_date).days
            if 0 <= days_remaining < 3:
                notifications.append(f"Task '{task.name}' is due in {days_remaining} day(s).")
    return notifications


def notify_overdue_tasks(tasks: List[Task], current_date: date) -> List[str]:
    """Notify of overdue tasks."""
    notifications = []
    for task in tasks:
        if task.status.lower() != "completed" and task.deadline < current_date:
            days_overdue = (current_date - task.deadline).days
            notifications.append(f"Task '{task.name}' is overdue by {days_overdue} day(s)!")
    return notifications


def check_schedule_conflicts(tasks: List[Task], new_task: Task) -> bool:
    """Check if two tasks share same deadline."""
    return any(task.deadline == new_task.deadline for task in tasks)
