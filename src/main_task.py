from datetime import date
from typing import List, Optional
from src.sub_task import SubTask
from src.task_id_manager import next_task_id


class Task:
    """Represents a single task in STM."""
    def __init__(self, task_id: int, name: str, category: str,
                 priority: str, deadline: date, status: str = "Pending",
                 recurrence: str | None = None, parent_id: int | None = None):
        self.task_id = task_id
        self.name = name
        self.category = category
        self.priority = priority
        self.deadline = deadline
        self.status = status
        self.recurrence = recurrence
        self.parent_id = parent_id
        self.subtask: List[SubTask] = []

    def add_subtask(self, subtask: SubTask) -> None:
        """Attach a subtask to this task."""
        self.subtask.append(subtask)

    def mark_complete(self) -> bool:
        """Mark complete only if all subtasks done."""
        if self.subtask:
            for subtask in self.subtask:
                if subtask.status != "Completed":
                    return False
        self.status = "Completed"
        return True

def add_task(name: str, category: str, priority: str, deadline: date,
             recurrence: str | None = None, parent_id: int | None = None) -> Task:
    """Create and return a Task with optional recurrence or parent."""
    return Task(next_task_id(), name, category, priority, deadline,
                recurrence=recurrence, parent_id=parent_id)

def edit_task(task: Task, new_name: Optional[str] = None,
              new_category: Optional[str] = None,
              new_priority: Optional[str] = None,
              new_deadline: Optional[date] = None) -> Task:
    """Edit in-place while preserving subtasks."""
    if new_name:
        task.name = new_name
    if new_category:
        task.category = new_category
    if new_priority:
        task.priority = new_priority
    if new_deadline:
        task.deadline = new_deadline
    return task

def delete_task(tasks: List[Task], task_id: int) -> bool:
    """Delete task by ID."""
    for task in tasks:
        if task.task_id == task_id:
            tasks.remove(task)
            return True
    return False
