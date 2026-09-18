import os
import time
import unittest
from datetime import date
from src.main_task import Task
from src.data_storage import save_to_json, load_from_json
from src.analytics import get_category_summary


class TestPerformance(unittest.TestCase):
    """
    Performance tests for Smart Task Manager (STM)
    Ensures scalability and speed of core operations:
    - JSON save and load (data persistence)
    - Analytics computation (category summary)
    """

    def setUp(self):
        """Prepare a large dataset for performance measurement."""
        self.big_tasks = [
            Task(i, f"Task{i}", "Work", "Low", date(2025, 12, 12))
            for i in range(10000)
        ]
        self.file = "performance_test.json"
        # Pre-save file for load test (so test_load_json_performance is independent)
        save_to_json(self.big_tasks, self.file)

    def tearDown(self):
        """Clean up generated JSON file after each test."""
        if os.path.exists(self.file):
            os.remove(self.file)

    # --- JSON Saving Performance ---
    def test_save_json_performance(self):
        """Saving 10k tasks should complete under 1 second."""
        start = time.perf_counter()
        save_to_json(self.big_tasks, self.file)
        elapsed = time.perf_counter() - start
        self.assertTrue(
            elapsed < 1.0,
            f"[!] Performance issue: saving took {elapsed:.2f}s (expected <1s)",
        )

    # --- JSON Loading Performance ---
    def test_load_json_performance(self):
        """Loading 10k tasks should complete under 1 second."""
        start = time.perf_counter()
        load_from_json(self.file)
        elapsed = time.perf_counter() - start
        self.assertTrue(
            elapsed < 1.0,
            f"[!] Performance issue: loading took {elapsed:.2f}s (expected <1s)",
        )

    # --- Analytics Performance (Time) ---
    def test_analytics_performance_time(self):
        """Category summary computation for 10k tasks should complete under 0.5s."""
        start = time.perf_counter()
        get_category_summary(self.big_tasks)
        elapsed = time.perf_counter() - start
        self.assertTrue(
            elapsed < 0.5,
            f"[!] Performance issue: analytics took {elapsed:.2f}s (expected <0.5s)",
        )

    # --- Analytics Correctness (Functional Check) ---
    def test_analytics_correctness(self):
        """Verify analytics results remain accurate for large datasets."""
        summary = get_category_summary(self.big_tasks)
        self.assertEqual(
            summary["Work"], 10000, "Expected all tasks counted under 'Work'."
        )

