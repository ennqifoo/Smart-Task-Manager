import unittest
from datetime import date
from src.sub_task import SubTask

'''
Possible tests:
T = when the scenarios are True
F = when the scenarios are False

A = can_mark_complete() returns True
B = current status == "Pending"

Decision: return True only if both (A and B) are True

T1: A=T, B=T, Outcome=True
T2: A=F, B=T, Outcome=False
T3: A=T, B=F, Outcome=True (already completed, no change)

Independent pairs:
A: (1,2)
B: (1,3)

Possible minimal MC/DC set: T1, T2, T3
'''

class TestSubTaskMarkComplete(unittest.TestCase):

    # --- T1: Prerequisite met & status pending (A=T, B=T) ------
    def test_T1_return_value_when_prerequisite_met_and_pending(self):
        s = SubTask(1, 1, "Sub", "High", date(2025, 10, 20))
        result = s.mark_complete([])
        self.assertTrue(result, "Expected True because prerequisite met and status pending")

    def test_T1_status_change_when_prerequisite_met_and_pending(self):
        s = SubTask(1, 1, "Sub", "High", date(2025, 10, 20))
        s.mark_complete([])
        self.assertEqual(s.status, "Completed", "Expected status to update to 'Completed' when prerequisite met and pending")

    # --- T2: Prerequisite unmet but status pending (A=F, B=T) --
    def test_T2_return_value_when_prerequisite_unmet_and_pending(self):
        s = SubTask(1, 1, "Sub", "High", date(2025, 10, 20), prerequisite_id=3)
        result = s.mark_complete([])  # prerequisite not completed
        self.assertFalse(result, "Expected False because prerequisite unmet even though status is pending")

    def test_T2_status_remains_pending_when_prerequisite_unmet(self):
        s = SubTask(1, 1, "Sub", "High", date(2025, 10, 20), prerequisite_id=3)
        s.mark_complete([])  # prerequisite not completed
        self.assertEqual(s.status, "Pending", "Expected status to remain 'Pending' when prerequisite unmet")

    # --- T3: Already completed (A=T, B=F) -----
    def test_T3_return_value_when_already_completed(self):
        s = SubTask(1, 1, "Sub", "High", date(2025, 10, 20))
        s.status = "Completed"
        result = s.mark_complete([])
        self.assertTrue(result, "Expected True because task already completed (no change needed)")

    def test_T3_status_unchanged_when_already_completed(self):
        s = SubTask(1, 1, "Sub", "High", date(2025, 10, 20))
        s.status = "Completed"
        s.mark_complete([])
        self.assertEqual(s.status, "Completed", "Expected status to remain 'Completed' when already completed")
