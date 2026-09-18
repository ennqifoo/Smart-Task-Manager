import unittest
from datetime import date
from src.main_task import add_task, Task


class TestAddTask(unittest.TestCase):

    def setUp(self):
        """Create a reusable valid Task object before each test."""
        self.expected_name = "A"
        self.expected_category = "Work"
        self.expected_priority = "High"
        self.expected_deadline = date(2025, 10, 20)
        self.task = add_task(
            self.expected_name,
            self.expected_category,
            self.expected_priority,
            self.expected_deadline
        )

    def test_task_name_is_correct(self):
        """Check if the created task name matches input."""
        self.assertEqual(
            self.task.name,
            self.expected_name,
            "Expected created Task to have correct name from input"
        )

    def test_task_category_is_correct(self):
        """Check if the created task category matches input."""
        self.assertEqual(
            self.task.category,
            self.expected_category,
            "Expected created Task to have correct category from input"
        )

    def test_task_priority_is_correct(self):
        """Check if the created task priority matches input."""
        self.assertEqual(
            self.task.priority,
            self.expected_priority,
            "Expected created Task to have correct priority from input"
        )

    def test_task_deadline_is_correct(self):
        """Check if the created task deadline matches input."""
        self.assertEqual(
            self.task.deadline,
            self.expected_deadline,
            "Expected created Task to have correct deadline from input"
        )
