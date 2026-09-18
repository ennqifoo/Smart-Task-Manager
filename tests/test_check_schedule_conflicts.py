import unittest
from datetime import date
from src.notification import check_schedule_conflicts
from src.main_task import Task


class TestCheckScheduleConflicts(unittest.TestCase):

    def setUp(self):
        """Create reusable task objects for conflict testing."""
        self.deadline_conflict = date(2025, 10, 20)
        self.deadline_no_conflict = date(2025, 10, 25)

        # Existing task with a specific deadline
        self.existing_task = Task(1, "A", "Work", "High", self.deadline_conflict)

        # New task with the same deadline (conflict)
        self.new_task_conflict = Task(2, "B", "Work", "High", self.deadline_conflict)

        # New task with a different deadline (no conflict)
        self.new_task_no_conflict = Task(3, "C", "Work", "High", self.deadline_no_conflict)

    # --- Conflict found ------
    def test_conflict_found_returns_true(self):
        """Should return True when another task shares the same deadline."""
        tasks = [self.existing_task]
        result = check_schedule_conflicts(tasks, self.new_task_conflict)
        self.assertTrue(result, "Expected True because both tasks share the same deadline (conflict detected)")

    # --- No conflict -----------
    def test_no_conflict_returns_false(self):
        """Should return False when no existing task shares the same deadline."""
        tasks = [self.existing_task]
        result = check_schedule_conflicts(tasks, self.new_task_no_conflict)
        self.assertFalse(result, "Expected False because no existing task shares the deadline")
