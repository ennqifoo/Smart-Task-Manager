import unittest
from datetime import date
from src.main_task import Task
from src.analytics import get_category_summary


class TestGetCategorySummary(unittest.TestCase):

    def setUp(self):
        """Create reusable sample tasks for category summary tests."""
        self.t1 = Task(1, "A", "Work", "High", date(2025, 10, 20))
        self.t2 = Task(2, "B", "Work", "High", date(2025, 10, 21))
        self.t3 = Task(3, "C", "Personal", "Low", date(2025, 10, 22))

    # --- Empty list -----------
    def test_empty_list_returns_empty_dict(self):
        """When task list is empty, function should return {}."""
        result = get_category_summary([])
        self.assertEqual(result, {}, "Expected empty dictionary when task list is empty")

    # --- Non-empty list -------
    def test_multiple_tasks_grouped_by_category(self):
        """When multiple tasks exist, group counts correctly by category."""
        tasks = [self.t1, self.t2, self.t3]
        result = get_category_summary(tasks)
        expected = {"Work": 2, "Personal": 1}
        self.assertEqual(result, expected, "Expected correct category counts: {'Work': 2, 'Personal': 1}")
