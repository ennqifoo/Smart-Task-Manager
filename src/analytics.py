from datetime import date, timedelta
from typing import List, Dict
from .main_task import Task


def calculate_completion_rate(tasks: List[Task]) -> float:
    """Calculate task completion rate as percentage."""
    if not tasks:
        return 0.0
    completed_count = sum(1 for task in tasks if task.status.lower() == "completed")
    return (completed_count / len(tasks)) * 100


def get_task_summary(tasks: List[Task]) -> Dict[str, int]:
    """Get comprehensive task statistics in single pass for performance."""
    if not tasks:
        return {"total": 0, "completed": 0, "pending": 0, "overdue": 0}

    today = date.today()
    completed_count = pending_count = overdue_count = 0

    for task in tasks:
        status = task.status.lower()
        if status == "completed":
            completed_count += 1
        elif status == "pending":
            pending_count += 1
            if task.deadline < today:
                overdue_count += 1

    return {
        "total": len(tasks),
        "completed": completed_count,
        "pending": pending_count,
        "overdue": overdue_count
    }


def get_summary(tasks: List[Task]) -> Dict[str, int]:
    """Backward compatibility wrapper for get_task_summary."""
    return get_task_summary(tasks)


def get_category_summary(tasks: List[Task]) -> Dict[str, int]:
    """Get task count by category."""
    category_counts: Dict[str, int] = {}
    for task in tasks:
        category_counts[task.category] = category_counts.get(task.category, 0) + 1
    return category_counts


def calculate_completion_streaks(tasks: List[Task], current_date: date) -> int:
    """Count consecutive days with at least one completed task."""
    streak_count = 0
    check_date = current_date

    while True:
        has_completion = any(
            task.status.lower() == "completed" and task.deadline == check_date
            for task in tasks
        )
        if has_completion:
            streak_count += 1
            check_date -= timedelta(days=1)
        else:
            break
    return streak_count
