import unittest
from datetime import date, timedelta
from src.notification import notify_upcoming_deadlines
from src.main_task import Task

'''
Possible tests:
T = when the scenarios are True
F = when the scenarios are False

A = status != "Completed"
B = 0 <= days_remaining < 3

Decision: return True only if (A and B) are both True

Boundary Values:
days_remaining = 0, 1, 2 → notify
days_remaining = 3 → do not notify

T1: A=T, B=T (0 days), Outcome=True
T2: A=T, B=T (2 days), Outcome=True
T3: A=T, B=F (3 days), Outcome=False
T4: A=F, B=T, Outcome=False

Independent pairs:
A: (1,4)
B: (2,3)

Possible minimal MC/DC set: T1, T2, T3, T4
'''

class TestNotifyUpcomingDeadlines(unittest.TestCase):

    def setUp(self):
        """Create reusable date references and base Task objects."""
        self.today = date.today()
        self.due_today = Task(1, "Task 1", "Work", "High", self.today)
        self.due_in_two_days = Task(2, "Task 2", "Work", "High", self.today + timedelta(days=2))
        self.due_in_three_days = Task(3, "Task 3", "Work", "High", self.today + timedelta(days=3))
        self.completed_due_soon = Task(4, "Task 4", "Work", "High", self.today + timedelta(days=1), status="Completed")

    # --- T1: A=True, B=True (due today) ----------
    def test_T1_due_today_triggers_notification(self):
        """BVA: Task due today (0 days) should trigger notification."""
        messages = notify_upcoming_deadlines([self.due_today], self.today)
        has_msg = any("due in 0" in msg for msg in messages)
        self.assertTrue(has_msg, "Expected notification for task due today (0 days remaining)")

    # --- T2: A=True, B=True (due in 2 days) ----------
    def test_T2_due_in_two_days_triggers_notification(self):
        """BVA: Task due in 2 days should trigger notification."""
        messages = notify_upcoming_deadlines([self.due_in_two_days], self.today)
        has_msg = any("due in 2" in msg for msg in messages)
        self.assertTrue(has_msg, "Expected notification for task due in 2 days (within 3-day window)")

    # --- T3: A=True, B=False (due in 3 days) -------
    def test_T3_due_in_three_days_no_notification(self):
        """BVA: Task due in 3 days should not trigger notification."""
        messages = notify_upcoming_deadlines([self.due_in_three_days], self.today)
        self.assertFalse(messages, "Expected no notification for task due in 3 days (outside 3-day window)")

    # --- T4: A=False, B=True (completed but due soon) -----
    def test_T4_completed_task_no_notification(self):
        """Completed task within 3 days should not trigger notification."""
        messages = notify_upcoming_deadlines([self.completed_due_soon], self.today)
        self.assertFalse(messages, "Expected no notification for completed task even if due soon")
