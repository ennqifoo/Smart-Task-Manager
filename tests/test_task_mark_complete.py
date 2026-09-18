import unittest
from datetime import date
from src.main_task import Task
from src.sub_task import SubTask

'''
Possible tests:
T = when the scenarios are True
F = when the scenarios are False

A = has subtasks
B = all subtasks completed

Decision: return True if (not A) or (A and B)

T1: A=F, –, Outcome=True
T2: A=T, B=T, Outcome=True
T3: A=T, B=F, Outcome=False

Independent pairs:
A: (1,2)
B: (2,3)

Possible minimal MC/DC set: T1, T2, T3
'''

class TestTaskMarkComplete(unittest.TestCase):

    def setUp(self):
        """Create reusable Task and SubTask templates for MC/DC testing."""
        self.main_task = Task(1, "Main", "Work", "High", date(2025, 10, 20))
        self.completed_subtask = SubTask(1, 1, "Sub1", "High", date(2025, 10, 19))
        self.completed_subtask.status = "Completed"
        self.pending_subtask = SubTask(2, 1, "Sub2", "High", date(2025, 10, 19))
        self.pending_subtask.status = "Pending"

    # --- T1: A=False (no subtasks) -------
    def test_T1_no_subtasks_returns_true(self):
        """No subtasks = mark_complete() should return True."""
        result = self.main_task.mark_complete()
        self.assertTrue(result, "Expected True when main task has no subtasks")

    # --- T2: A=True, B=True (all subtasks completed) ----
    def test_T2_all_subtasks_completed_returns_true(self):
        """All subtasks completed = mark_complete() should return True."""
        self.main_task.add_subtask(self.completed_subtask)
        result = self.main_task.mark_complete()
        self.assertTrue(result, "Expected True when all subtasks are completed")

    # --- T3: A=True, B=False (some subtasks pending) --
    def test_T3_some_subtasks_pending_returns_false(self):
        """Some subtasks pending = mark_complete() should return False."""
        self.main_task.add_subtask(self.pending_subtask)
        result = self.main_task.mark_complete()
        self.assertFalse(result, "Expected False when not all subtasks are completed")
