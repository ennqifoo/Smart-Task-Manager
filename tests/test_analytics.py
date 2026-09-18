import unittest
from datetime import date
from src.analytics import get_summary, calculate_completion_rate, get_category_summary
from src.main_task import Task

'''
Testing Type: White-box (Path Testing)
Goal: Verify computation and summary logic for analytics functions.
Functions: get_summary(), calculate_completion_rate(), get_category_summary()
'''

class TestAnalytics(unittest.TestCase):

    def setUp(self):
        """Set up reusable Task examples for all analytics tests."""
        # Task 1: Future task, completed
        self.task1 = Task(1, "Task 1", "Work", "High", date(2025, 12, 12))
        self.task1.status = "Completed"

        # Task 2: Past-due task
        self.task2 = Task(2, "Task 2", "Personal", "Medium", date(2020, 1, 1))
        self.task2.status = "Pending"

        # Task 3: Another future task (for category tests)
        self.task3 = Task(3, "Task 3", "Personal", "Low", date(2025, 12, 14))

    # --- get_summary() ------------
    def test_get_summary_empty_tasks(self):
        """Empty task list should produce all zero summary values."""
        result = get_summary([])
        expected = {'total': 0, 'completed': 0, 'pending': 0, 'overdue': 0}
        self.assertEqual(result, expected, "Expected zeroed summary for empty task list")

    def test_get_summary_with_tasks(self):
        """Mixed completed and overdue tasks should produce correct summary counts."""
        tasks = [self.task1, self.task2]
        result = get_summary(tasks)
        expected = {'total': 2, 'completed': 1, 'pending': 1, 'overdue': 1}
        self.assertEqual(result, expected, "Expected summary to count completed=1, pending=1, overdue=1")

    # --- calculate_completion_rate() --------
    def test_calculate_completion_rate_empty(self):
        """Empty list should yield 0.0% completion rate."""
        result = calculate_completion_rate([])
        self.assertEqual(result, 0.0, "Expected 0.0% completion rate for empty list")

    def test_calculate_completion_rate_with_tasks(self):
        """Completion rate should reflect proportion of completed tasks."""
        tasks = [self.task1, self.task3]  # 1 completed, 1 pending
        result = calculate_completion_rate(tasks)
        self.assertEqual(result, 50.0, "Expected 50.0% completion rate for one completed out of two")

    # --- get_category_summary() --------------
    def test_get_category_summary_empty(self):
        """Empty list should return an empty dictionary."""
        result = get_category_summary([])
        self.assertEqual(result, {}, "Expected empty dictionary for empty task list")

    def test_get_category_summary_with_tasks(self):
        """Should group tasks by category correctly."""
        tasks = [self.task1, self.task2, self.task3]
        result = get_category_summary(tasks)
        expected = {"Work": 1, "Personal": 2}
        self.assertEqual(result, expected, "Expected grouped category counts {'Work':1, 'Personal':2}")
