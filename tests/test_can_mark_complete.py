import unittest
from datetime import date
from src.sub_task import SubTask

'''
Possible tests:
T = when the scenarios are True
F = when the scenarios are False

A = prerequisite_id is None
B = prerequisite_id in completed_ids

Decision: return True only if (A or B) is True

T1: A=T, B=–, Outcome=True
T2: A=F, B=T, Outcome=True
T3: A=F, B=F, Outcome=False

Independent pairs:
A: (1,3)
B: (2,3)

Possible minimal MC/DC set: T1, T2, T3
'''

class TestCanMarkComplete(unittest.TestCase):

    def setUp(self):
        """Initialize reusable SubTask objects for each MC/DC condition."""
        self.date_sample = date(2025, 10, 20)
        # Case with no prerequisite
        self.no_prerequisite_task = SubTask(1, 1, "A", "High", self.date_sample)
        # Case with prerequisite ID = 2
        self.with_prerequisite_task = SubTask(2, 1, "B", "High", self.date_sample, prerequisite_id=2)

    # --- T1: A=True, B=– (no prerequisite) ----------
    def test_T1_no_prerequisite_returns_true(self):
        """Should return True when there is no prerequisite."""
        result = self.no_prerequisite_task.can_mark_complete([])
        self.assertTrue(result, "Expected True since task has no prerequisite")

    # --- T2: A=False, B=True (prerequisite completed) ----
    def test_T2_prerequisite_completed_returns_true(self):
        """Should return True when prerequisite is in completed_ids."""
        result = self.with_prerequisite_task.can_mark_complete([2])
        self.assertTrue(result, "Expected True since prerequisite ID 2 is marked completed")

    # --- T3: A=False, B=False (prerequisite not completed) ---------
    def test_T3_prerequisite_not_completed_returns_false(self):
        """Should return False when prerequisite is not completed."""
        result = self.with_prerequisite_task.can_mark_complete([])
        self.assertFalse(result, "Expected False since prerequisite not completed and not None")
