from datetime import date
from typing import List, Optional


class SubTask:
    """Subtask model with prerequisite logic."""
    def __init__(self, subtask_id: int, parent_task_id: int,
                 name: str, priority: str, deadline: date,
                 prerequisite_id: Optional[int] = None,
                 status: str = "Pending"):
        self.subtask_id = subtask_id
        self.parent_task_id = parent_task_id
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.prerequisite_id = prerequisite_id
        self.status = status

    def can_mark_complete(self, completed_ids: List[int]) -> bool:
        """Check if prerequisite met before completion."""
        if self.prerequisite_id is None:
            return True
        return self.prerequisite_id in completed_ids

    def mark_complete(self, completed_ids: List[int]) -> bool:
        """Mark subtask complete if prerequisites are done."""
        if self.can_mark_complete(completed_ids):
            self.status = "Completed"
            return True
        return False
