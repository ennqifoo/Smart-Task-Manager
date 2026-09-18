import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from src.menu_handlers import (
    handle_add_main_task, handle_view_tasks, handle_view_notifications,
    get_valid_parent_task, get_valid_task_by_id, display_analytics,
    handle_add_task, handle_add_subtask, handle_view_tasks,
    handle_view_notifications, handle_edit_task, handle_delete_task,
    handle_mark_complete, get_valid_task_by_id
)
from src.main_task import Task
from src.sub_task import SubTask

class TestMenuHandlers(unittest.TestCase):

    def setUp(self):
        """Initialize reusable task list for all menu handler tests."""
        self.tasks = []

    # --- handle_add_main_task() ------------------------------------------
    @patch('src.menu_handlers.get_task_input')
    @patch('src.menu_handlers.user_input.read_yes_no')
    def test_handle_add_main_task_success(self, mock_read_yes_no, mock_get_task_input):
        """Should successfully add a valid main task."""
        mock_get_task_input.return_value = ("Test Task", "Work", "High", "2025-12-12")
        mock_read_yes_no.return_value = False
        result = handle_add_main_task(self.tasks)
        self.assertTrue(result, "Expected handle_add_main_task() to return True for valid input")

    @patch('src.menu_handlers.get_task_input')
    def test_handle_add_main_task_past_deadline_then_valid(self, mock_get_task_input):
        """Should reject past deadline and accept future deadline on retry."""
        mock_get_task_input.side_effect = [
            ("Test Task", "Work", "High", "2020-01-01"),  # invalid past deadline
            ("Test Task", "Work", "High", "2025-12-12")   # valid future deadline
        ]
        with patch('src.menu_handlers.user_input.read_yes_no', return_value=False):
            result = handle_add_main_task(self.tasks)
        self.assertTrue(result, "Expected function to return True after retrying with valid future deadline")

    # --- display_analytics() ---------------------------------------------
    def test_display_analytics_prints_summary(self):
        """Should print analytics summary when tasks exist."""
        task1 = Task(1, "Task 1", "Work", "High", date(2025, 12, 12))
        task2 = Task(2, "Task 2", "Personal", "Medium", date(2025, 12, 13))
        task1.status = "Completed"
        self.tasks.extend([task1, task2])
        with patch('src.menu_handlers.console.print') as mock_print:
            display_analytics(self.tasks)
            self.assertTrue(mock_print.called, "Expected analytics summary to be printed")

    # --- get_valid_parent_task() -----------
    @patch('builtins.input')
    def test_get_valid_parent_task_success(self, mock_input):
        """Should return valid parent task when ID exists."""
        task = Task(1, "Parent Task", "Work", "High", date(2025, 12, 12))
        self.tasks.append(task)
        mock_input.return_value = "1"
        result = get_valid_parent_task(self.tasks)
        self.assertEqual(result, task, "Expected valid parent Task object returned for input ID '1'")

    @patch('builtins.input')
    def test_get_valid_parent_task_invalid_then_valid(self, mock_input):
        """Should reject invalid input and accept valid task ID."""
        task = Task(1, "Parent Task", "Work", "High", date(2025, 12, 12))
        self.tasks.append(task)
        mock_input.side_effect = ["abc", "1"]
        with patch('builtins.print'):
            result = get_valid_parent_task(self.tasks)
        self.assertEqual(result, task, "Expected task returned after retrying with valid ID")

    # --- get_valid_task_by_id() ------------------------------------------
    @patch('builtins.input')
    def test_get_valid_task_by_id_cancel(self, mock_input):
        """Should return None when user cancels with 'c'."""
        mock_input.return_value = "c"
        with patch('builtins.print'):
            result = get_valid_task_by_id(self.tasks, "Enter ID: ")
        self.assertEqual(result, None, "Expected None when user cancels task ID input")

    @patch('builtins.input')
    def test_get_valid_task_by_id_success(self, mock_input):
        """Should return correct task object for valid ID input."""
        task = Task(1, "Test Task", "Work", "High", date(2025, 12, 12))
        self.tasks.append(task)
        mock_input.return_value = "1"
        result = get_valid_task_by_id(self.tasks, "Enter ID: ")
        self.assertEqual(result, task, "Expected valid Task object returned for input ID '1'")

    # ----------- handle view task --------------------------------
    @patch("src.menu_handlers.display_tasks")
    def test_handle_view_tasks_prints_tasks(self, mock_display):
        """Should display all tasks when list is not empty."""
        tasks = [Task(1, "Task A", "Work", "High", date(2025, 12, 12))]
        handle_view_tasks(tasks)
        # display_tasks should have been called once
        called = mock_display.called
        self.assertTrue(called, "handle_view_tasks() should call display_tasks() when tasks exist.")

    # --- handle_view_notifications() ---------------------------
    @patch("src.menu_handlers.notify_upcoming_deadlines")
    @patch("src.menu_handlers.notify_overdue_tasks")
    def test_handle_view_notifications_calls_notify(self, mock_overdue, mock_upcoming):
        """Should call both notification functions."""
        handle_view_notifications([])
        both_called = mock_overdue.called and mock_upcoming.called
        self.assertTrue(both_called, "handle_view_notifications() should call both overdue and upcoming checks.")

    # -------- handle add task --------------
    @patch("builtins.input", side_effect=["m"])
    @patch("src.menu_handlers.handle_add_main_task", return_value=True)
    def test_handle_add_task_main(self, mock_main, mock_input):
        """Should call handle_add_main_task for 'm' input."""
        tasks = []
        handle_add_task(tasks)
        self.assertTrue(mock_main.called, "handle_add_task() should call handle_add_main_task() for 'm'.")


    @patch("builtins.input", side_effect=["s"])
    @patch("src.menu_handlers.handle_add_subtask", return_value=True)
    def test_handle_add_task_sub(self, mock_sub, mock_input):
        """Should call handle_add_subtask for 's' input."""
        tasks = []
        handle_add_task(tasks)
        self.assertTrue(mock_sub.called, "handle_add_task() should call handle_add_subtask() for 's' input.")

    # --------- handle add subtask --------------------
    @patch("src.menu_handlers.get_valid_parent_task")
    @patch("src.menu_handlers.get_subtask_input", return_value=("SubTask A", date(2025, 12, 12)))
    def test_handle_add_subtask_adds_subtask(self, mock_get_subtask_input, mock_get_valid_parent):
        parent = Task(1, "Parent", "Work", "High", date(2025, 12, 12))
        tasks = [parent]
        mock_get_valid_parent.return_value = parent
        handle_add_subtask(tasks)
        self.assertTrue(
            isinstance(parent.subtask[0], SubTask),
            "handle_add_subtask() should add a SubTask to parent task."
        )

    # -------------- handle edit task ----------------
    @patch("builtins.input", side_effect=["m", "1", "New name", "5", "", "", "", ""])
    @patch("src.menu_handlers.get_valid_task_by_id")
    @patch("src.menu_handlers.edit_task")
    def test_handle_edit_task_updates_existing(self, mock_edit, mock_get, mock_input):
        """Should edit task successfully when valid task ID provided."""
        task = Task(1, "Old", "Work", "Low", date(2025, 12, 12))
        tasks = [task]
        mock_get.return_value = task

        handle_edit_task(tasks)

        self.assertTrue(mock_edit.called, "handle_edit_task() should call edit_task() on valid task.")


    # -------------- handle delete task ----------------
    @patch("src.menu_handlers.input", return_value="m")
    @patch("src.menu_handlers.handle_delete_main_task", return_value=True)
    def test_handle_delete_task_removes_existing(self, mock_delete_main, mock_input):
        """Should call handle_delete_main_task() for 'm' input in handle_delete_task."""
        tasks = [Task(1, "Dummy", "Work", "Low", date(2025, 12, 12))]
        handle_delete_task(tasks)
        self.assertTrue(
            mock_delete_main.called,
            "handle_delete_task() should delegate to handle_delete_main_task() for 'm'."
        )

    # -------------- handle mark complete ----------------
    @patch("builtins.input", side_effect=["99", "1"])
    def test_get_valid_parent_task_invalid_then_valid(self, mock_input):
        """Should retry until valid parent task ID is entered."""
        parent = Task(1, "T", "C", "H", date(2025,12,12))
        tasks = [parent]
        result = get_valid_parent_task(tasks)
        self.assertEqual(result, parent, "Expected valid parent returned after retry.")

    @patch("builtins.input", side_effect=["0", "1"])
    def test_get_valid_task_by_id_invalid_then_valid(self, mock_input):
        """Should return correct task after invalid attempt."""
        t = Task(1, "A", "B", "C", date(2025,12,12))
        tasks = [t]
        result = get_valid_task_by_id(tasks, "Enter Task ID: ")
        self.assertEqual(result, t, "Expected get_valid_task_by_id to return task after retry.")

    @patch("src.menu_handlers.user_input.read_integer_range", return_value=2)
    @patch("src.menu_handlers.user_input.read_yes_no", return_value=True)
    @patch("src.menu_handlers.get_task_input", return_value=("X", "W", "H", "2025-12-12"))
    def test_handle_add_main_task_recurring(self, mock_input, mock_yes, mock_int):
        """Should accept recurring task successfully."""
        ok = handle_add_main_task(self.tasks)
        self.assertTrue(ok, "Expected recurring main task creation to succeed.")
