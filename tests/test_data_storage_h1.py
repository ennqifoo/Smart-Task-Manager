import os
import json
import unittest
from datetime import date
from hypothesis import given, strategies as st
from src.main_task import Task
from src.data_storage import save_to_json, load_from_json

"""H1 features: Tests for data storage module using Hypothesis for property-based testing."""

class TestDataStorage(unittest.TestCase):

    @given(
        names=st.lists(st.text(min_size=1, max_size=10), min_size=1, max_size=10),
        priorities=st.lists(st.sampled_from(["Low", "Medium", "High"]), min_size=1, max_size=10),
        categories=st.lists(st.sampled_from(["Work", "Home", "Study"]), min_size=1, max_size=10)
    )
    def test_save_and_load_random_tasks(self, names, priorities, categories):
        """Hypothesis-based: JSON save/load should maintain task integrity."""
        test_file = "test_random_tasks.json"

        # Build random tasks from generated data
        tasks = []
        for i in range(min(len(names), len(priorities), len(categories))):
            tasks.append(Task(i+1, names[i], categories[i], priorities[i], date(2025, 12, 12)))

        # Save and load using data_storage
        save_to_json(tasks, test_file)
        loaded = load_from_json(test_file)

        # Assertions
        self.assertEqual(len(tasks), len(loaded), "Loaded task count should match original.")
        if tasks:  # only compare attributes if non-empty
            self.assertEqual(tasks[0].name, loaded[0].name, "Task name should persist correctly.")
            self.assertEqual(tasks[0].priority, loaded[0].priority, "Task priority should persist correctly.")
            self.assertEqual(tasks[0].category, loaded[0].category, "Task category should persist correctly.")

        os.remove(test_file)
