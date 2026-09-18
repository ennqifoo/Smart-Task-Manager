import unittest
from datetime import date
from src.main_task import Task, delete_task


class TestDeleteTask(unittest.TestCase):

    # --- Path 1: task_id found and deleted --------
    def test_return_value_when_task_found(self):
        """Expect True when the task with given ID is found and removed."""
        t = Task(1, "A", "Work", "High", date(2025, 10, 20))
        tasks = [t]
        result = delete_task(tasks, 1)
        self.assertTrue(result, "Expected True when delete_task() successfully removes existing task")

    def test_task_list_empty_after_deletion(self):
        """Ensure the task is actually removed from the list after successful deletion."""
        t = Task(1, "A", "Work", "High", date(2025, 10, 20))
        tasks = [t]
        delete_task(tasks, 1)
        self.assertEqual(tasks, [], "Expected task list to become empty after deletion of existing task")

    # --- Path 2: task_id not found --------------
    def test_return_value_when_task_not_found(self):
        """Expect False when trying to delete a non-existent task ID."""
        t = Task(1, "A", "Work", "High", date(2025, 10, 20))
        tasks = [t]
        result = delete_task(tasks, 99)
        self.assertFalse(result, "Expected False when task ID does not exist in the list")

    def test_task_list_length_unchanged_when_not_found(self):
        """Ensure list length unchanged when ID not found."""
        t = Task(1, "A", "Work", "High", date(2025, 10, 20))
        tasks = [t]
        delete_task(tasks, 99)
        self.assertEqual(len(tasks), 1, "Expected same number of tasks after failed deletion")

    def test_task_list_content_unchanged_when_not_found(self):
        """Ensure the same task object remains after failed deletion."""
        t = Task(1, "A", "Work", "High", date(2025, 10, 20))
        tasks = [t]
        delete_task(tasks, 99)
        self.assertEqual(tasks[0].task_id, 1, "Expected existing task to remain in list after failed deletion")
