import unittest
from datetime import date, timedelta
from src.notification import notify_overdue_tasks
from src.main_task import Task

'''
Possible tests:
T = when the scenarios are True
F = when the scenarios are False

A = status != "Completed"
B = deadline < current_date

Decision: return True only if (A and B) are both True

T1: A=T, B=T, Outcome=True
T2: A=T, B=F, Outcome=False
T3: A=F, B=T, Outcome=False

Independent pairs:
A: (1,3)
B: (1,2)

Possible minimal MC/DC set: T1, T2, T3
'''

class TestNotifyOverdueTasks(unittest.TestCase):

    def setUp(self):
        """Initialize reusable date references and task templates."""
        self.today = date.today()
        self.yesterday = self.today - timedelta(days=1)
        self.tomorrow = self.today + timedelta(days=1)

        # Overdue pending task (A=T, B=T)
        self.overdue_pending = Task(1, "Overdue Pending", "Work", "High", self.yesterday, status="Pending")
        # Future pending task (A=T, B=F)
        self.future_pending = Task(2, "Future Pending", "Work", "High", self.tomorrow, status="Pending")
        # Completed overdue task (A=F, B=T)
        self.overdue_completed = Task(3, "Overdue Completed", "Work", "High", self.yesterday, status="Completed")

    # --- T1: A=True, B=True (overdue and not completed) ------------------
    def test_T1_overdue_not_completed_triggers_notification(self):
        """Task overdue and not completed → should generate overdue message."""
        messages = notify_overdue_tasks([self.overdue_pending], self.today)
        has_overdue_msg = any("overdue" in msg.lower() for msg in messages)
        self.assertTrue(has_overdue_msg, "Expected overdue notification for pending overdue task")

    # --- T2: A=True, B=False (not overdue yet) ---------------------------
    def test_T2_not_overdue_no_notification(self):
        """Task not yet overdue → should not trigger any message."""
        messages = notify_overdue_tasks([self.future_pending], self.today)
        self.assertFalse(messages, "Expected no notification for task not yet overdue")

    # --- T3: A=False, B=True (completed but overdue) ---------------------
    def test_T3_completed_overdue_no_notification(self):
        """Task completed even if overdue → should not trigger message."""
        messages = notify_overdue_tasks([self.overdue_completed], self.today)
        self.assertFalse(messages, "Expected no notification for completed overdue task")
