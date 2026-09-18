import unittest
from datetime import date
from src.main_task import Task
from src.analytics import get_summary, get_task_summary

class TestGetSummary(unittest.TestCase):

    def setUp(self):
        """Create a reusable completed task for summary comparison."""
        self.task = Task(1, "A", "Work", "High", date(2025, 10, 20), status="Completed")

    def test_wrapper_matches_get_task_summary(self):
        """get_summary() should return same result as get_task_summary() for same input."""
        result_summary = get_summary([self.task])
        result_direct = get_task_summary([self.task])
        self.assertEqual(result_summary, result_direct,
                         "Expected get_summary() output to match get_task_summary() exactly for same input")
