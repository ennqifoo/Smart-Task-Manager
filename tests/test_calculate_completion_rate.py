import unittest
from datetime import date
from src.main_task import Task
from src.analytics import calculate_completion_rate

class TestCalculateCompletionRate(unittest.TestCase):

    def setUp(self):
        """Create reusable Task objects for testing completion rates."""
        self.completed_task = Task(
            1, "A", "Work", "High", date(2025, 10, 20), status="Completed"
        )
        self.pending_task = Task(
            2, "B", "Work", "Low", date(2025, 10, 21), status="Pending"
        )

    # --- tasks list empty ---------
    def test_empty_list_returns_zero(self):
        """Empty list should return completion rate 0.0."""
        result = calculate_completion_rate([])
        self.assertEqual(result, 0.0, "Expected 0.0% completion rate for empty task list")

    # --- non-empty list --------------
    def test_partial_completion_rate(self):
        """One completed out of two tasks should yield 50.0%."""
        result = calculate_completion_rate([self.completed_task, self.pending_task])
        self.assertEqual(result, 50.0, "Expected 50.0% completion rate for one completed out of two tasks")

    def test_all_completed_rate(self):
        """All tasks completed should yield 100.0%."""
        result = calculate_completion_rate([self.completed_task, self.completed_task])
        self.assertEqual(result, 100.0, "Expected 100.0% completion rate when all tasks are completed")

    def test_none_completed_rate(self):
        """All tasks pending should yield 0.0%."""
        result = calculate_completion_rate([self.pending_task, self.pending_task])
        self.assertEqual(result, 0.0, "Expected 0.0% completion rate when all tasks are pending")
