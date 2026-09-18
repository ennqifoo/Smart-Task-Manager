import unittest
from datetime import date
from src.main_task import edit_task, Task

'''
Feasible paths:

"""
    Edit in-place while preserving subtasks.

    Path Testing Analysis:
    - Path 1: 41 -> 45 -> 46(F) -> 48(F) -> 50(F) -> 52(F) -> 54
        (No changes)
    - Path 2: 41 -> 45 -> 46(T) -> 47 -> 48(F) -> 50(F) -> 52(F) -> 54
        (Only name changed)
    - Path 3: 41 -> 45 -> 46(F) -> 48(T) -> 49 -> 50(F) -> 52(F) -> 54
        (Only category changed)
    - Path 4: 41 -> 45 -> 46(F) -> 48(F) -> 50(T) -> 51 -> 52(F) -> 54
        (Only priority changed)
    - Path 5: 41 -> 45 -> 46(F) -> 48(F) -> 50(F) -> 52(T) -> 53 -> 54
        (Only deadline changed)
    - Path 6: 41 -> 45 -> 46(T) -> 47 -> 48(T) -> 49 -> 50(T) -> 51 -> 52(T) -> 53 -> 54
        (All attributes changed)

    Testing Method: White-Box Testing (Path Testing)
    """
'''

class TestEditTask(unittest.TestCase):

    def setUp(self):
        """Create a reusable sample Task and common new values."""
        self.task = Task(1, "Old", "Work", "Low", date(2025, 10, 20))
        self.new_dead = date(2025, 11, 1)
        self.new_name = "New"
        self.new_category = "Study"
        self.new_priority = "High"

    # --- Path 1: No arguments changed --------------
    def test_no_changes(self):
        """Expect unchanged attributes when no arguments provided."""
        t = edit_task(self.task)
        self.assertEqual(t.name, "Old", "Expected task name to remain unchanged when no arguments provided")

    # --- Path 2: Only name changed --------
    def test_change_name_only(self):
        """Expect name updated, others unchanged."""
        t = edit_task(self.task, new_name=self.new_name)
        self.assertEqual(t.name, self.new_name, "Expected task name to update to new value")

    # --- Path 3: Only category changed ----
    def test_change_category_only(self):
        """Expect category updated, others unchanged."""
        t = edit_task(self.task, new_category=self.new_category)
        self.assertEqual(t.category, self.new_category, "Expected task category to update to new value")

    # --- Path 4: Only priority changed -----------
    def test_change_priority_only(self):
        """Expect priority updated, others unchanged."""
        t = edit_task(self.task, new_priority=self.new_priority)
        self.assertEqual(t.priority, self.new_priority, "Expected task priority to update to new value")

    # --- Path 5: Only deadline changed -------------
    def test_change_deadline_only(self):
        """Expect deadline updated, others unchanged."""
        t = edit_task(self.task, new_deadline=self.new_dead)
        self.assertEqual(t.deadline, self.new_dead, "Expected task deadline to update to new value")

    # --- Path 6: All fields changed (atomic checks per field) ------------
    def test_change_all_fields_name(self):
        """Check name change when all fields updated."""
        t = edit_task(self.task, new_name="All", new_category=self.new_category,
                      new_priority=self.new_priority, new_deadline=self.new_dead)
        self.assertEqual(t.name, "All", "Expected task name updated when all fields changed")

    # --- Additional checks for all fields changed (to improve coverage)------------
    def test_change_all_fields_category(self):
        """Check category change when all fields updated."""
        t = edit_task(self.task, new_name="All", new_category=self.new_category,
                      new_priority=self.new_priority, new_deadline=self.new_dead)
        self.assertEqual(t.category, self.new_category, "Expected category updated when all fields changed")

    def test_change_all_fields_priority(self):
        """Check priority change when all fields updated."""
        t = edit_task(self.task, new_name="All", new_category=self.new_category,
                      new_priority=self.new_priority, new_deadline=self.new_dead)
        self.assertEqual(t.priority, self.new_priority, "Expected priority updated when all fields changed")

    def test_change_all_fields_deadline(self):
        """Check deadline change when all fields updated."""
        t = edit_task(self.task, new_name="All", new_category=self.new_category,
                      new_priority=self.new_priority, new_deadline=self.new_dead)
        self.assertEqual(t.deadline, self.new_dead, "Expected deadline updated when all fields changed")
