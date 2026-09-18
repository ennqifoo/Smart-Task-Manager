import unittest
from datetime import date, timedelta
from src.main_task import Task
from src.analytics import calculate_completion_streaks

"""
Count consecutive days with at least one completed task.

    Path Testing Analysis:
    - Path 1: 52 → 54 → 55 → 57 → 58 → 62 → 66 → 67
        (No completed tasks; loop breaks immediately)
    - Path 2: 52 → 54 → 55 → 57 → 58 → 62(T) → 63 → 64 → 57 → 58 → 62(F) → 66 → 67
        (Single-day streak)
    - Path 3: 52 → 54 → 55 → 57 → 58 → 62(T) → 63 → 64 → [repeat for multiple days]
              → 57 → 58 → 62(F) → 66 → 67
        (Multi-day consecutive streak)
    - Path 4: 52 → 54 → 55 → 57 → 58 → 62(T) → 63 → 64 → 57 → 58 → 62(F) → 66 → 67
        (Non-consecutive completions reset streak)

    Testing Method: White-Box Testing (Path Testing)
"""

class TestCalculateCompletionStreaks(unittest.TestCase):

    def setUp(self):
        """Create reusable date references and base tasks."""
        self.today = date.today()
        # Completed tasks on consecutive days
        self.task_today = Task(1, "A", "Work", "High", self.today, status="Completed")
        self.task_yesterday = Task(2, "B", "Work", "High", self.today - timedelta(days=1), status="Completed")
        self.task_two_days_ago = Task(3, "C", "Work", "High", self.today - timedelta(days=2), status="Completed")
        # Pending task (not completed)
        self.pending_task = Task(4, "D", "Work", "High", self.today, status="Pending")

    # --- Path 1: No completed tasks ------------
    def test_no_completed_tasks_returns_zero(self):
        """No completed tasks → streak should be 0."""
        result = calculate_completion_streaks([self.pending_task], self.today)
        self.assertEqual(result, 0, "Expected streak count 0 when there are no completed tasks")

    # --- Path 2: One-day streak --------------------
    def test_single_day_streak_returns_one(self):
        """Only today’s task completed → streak = 1."""
        result = calculate_completion_streaks([self.task_today], self.today)
        self.assertEqual(result, 1, "Expected streak count 1 when only today’s task is completed")

    # --- Path 3: Multi-day streak -------
    def test_three_day_streak_returns_three(self):
        """Consecutive completions for three days → streak = 3."""
        tasks = [self.task_today, self.task_yesterday, self.task_two_days_ago]
        result = calculate_completion_streaks(tasks, self.today)
        self.assertEqual(result, 3, "Expected streak count 3 for three consecutive completed days")

    # --- Path 4: Non-consecutive completions reset streak -------
    def test_non_consecutive_completions_resets_streak(self):
        """Missed day should reset streak (e.g., skip yesterday)."""
        skipped_yesterday = Task(5, "E", "Work", "High", self.today - timedelta(days=2), status="Completed")
        result = calculate_completion_streaks([self.task_today, skipped_yesterday], self.today)
        self.assertEqual(result, 1, "Expected streak 1 when there’s a missed day between completions")
