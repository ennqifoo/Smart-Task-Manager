import unittest
from unittest import mock
from datetime import date
from src.ui import (
    main_menu, get_task_input, get_subtask_input,
    edit_task_menu, get_creation_options,
    display_tasks, display_notifications
)
from src.main_task import Task

class TestUI(unittest.TestCase):
    """Black-box tests for UI layer functions using EP, BVA, and Mocking."""

    # --- main_menu() -----
    '''
    BVA + EP:
    - Valid input 1–6 = accepted
    - Invalid (-1, 0, 7, "a") = re-prompt
    '''
    @mock.patch("builtins.input", side_effect=["0", "7", "a", "3"])
    def test_main_menu_valid_selection(self, mock_input):
        result = main_menu()
        self.assertEqual(result, 7, "Expected valid input '7' to be accepted after invalid retries")

    # --- get_task_input() -------
    '''
    EP + Mocking:
    - Valid name, category, priority, deadline = accepted TaskInput
    - Empty name = re-prompt handled
    '''
    @mock.patch("src.user_input.read_deadline", return_value="2025-10-20")
    @mock.patch("src.user_input.read_priority", return_value="High")
    @mock.patch("src.user_input.read_category", return_value="Work")
    @mock.patch("src.user_input.read_task_name", return_value="TestTask")
    def test_get_task_input_returns_correct_name(self, mock_name, mock_cat, mock_prio, mock_dead):
        result = get_task_input()
        self.assertEqual(result.name, "TestTask", "Expected task name to match mocked input 'TestTask'")

    @mock.patch("src.user_input.read_deadline", return_value="2025-10-20")
    @mock.patch("src.user_input.read_priority", return_value="High")
    @mock.patch("src.user_input.read_category", return_value="Work")
    @mock.patch("src.user_input.read_task_name", return_value="TestTask")
    def test_get_task_input_returns_correct_category(self, mock_name, mock_cat, mock_prio, mock_dead):
        result = get_task_input()
        self.assertEqual(result.category, "Work", "Expected task category to match mocked input 'Work'")

    # --- get_subtask_input() --------
    '''
    EP + Mocking:
    - Subtask deadline within parent = valid
    - Deadline after parent = re-prompt
    '''
    @mock.patch("src.user_input.read_deadline", side_effect=["2025-10-25", "2025-10-20"])
    @mock.patch("src.user_input.read_task_name", return_value="SubA")
    def test_get_subtask_input_reprompt_on_invalid_deadline(self, mock_name, mock_dead):
        parent_task = Task(1, "Main", "Work", "High", date(2025, 10, 22))
        result = get_subtask_input(parent_task)
        self.assertEqual(result.name, "SubA", "Expected subtask input to reprompt and return valid SubA after invalid deadline")

    # --- edit_task_menu() -------
    '''
    EP:
    - Valid field selection 1–4 = updates
    - Finish option 5 = exits menu
    '''
    @mock.patch("builtins.input", side_effect=["5"])
    def test_edit_task_menu_finish_option(self, mock_input):
        t = Task(1, "A", "Work", "Low", date(2025, 10, 20))
        result = edit_task_menu(t)
        self.assertEqual(len(result), 4, "Expected edit_task_menu to return list of 4 editable fields on exit")

    # --- get_creation_options() -----
    '''
    EP + Mocking:
    - Choose subtask flow = returns correct flags
    - Choose recurring flow = returns correct recurrence
    '''
    @mock.patch("src.user_input.read_yes_no", side_effect=[True, False])
    @mock.patch("builtins.input", side_effect=["1", ""])
    def test_get_creation_options_is_subtask_flag_true(self, mock_inp, mock_yn):
        """Verify subtask flag is correctly set when subtask flow chosen."""
        t = Task(1, "A", "Work", "Low", date(2025, 10, 20))
        tasks = [t]
        result = get_creation_options(tasks)
        self.assertTrue(result["is_subtask"], "Expected is_subtask to be True for subtask creation flow")

    @mock.patch("src.user_input.read_yes_no", side_effect=[True, False])
    @mock.patch("builtins.input", side_effect=["1", ""])
    def test_get_creation_options_recurrence_is_none(self, mock_inp, mock_yn):
        """Verify recurrence value equals None for subtask-only flow."""
        t = Task(1, "A", "Work", "Low", date(2025, 10, 20))
        tasks = [t]
        result = get_creation_options(tasks)
        self.assertEqual(result["recurrence"], None, "Expected recurrence to equal None for subtask-only flow")

    # --- display_tasks() --------
    '''
    EP:
    - Empty list = prints [No tasks available.]
    - Non-empty = displays task info
    '''
    def test_display_tasks_empty_list(self):
        """Ensure no crash and correct handling when task list is empty."""
        output = display_tasks([])
        self.assertEqual(output, None, "Expected display_tasks([]) to complete without errors")

    # --- display_notifications() -----
    '''
    EP:
    - No notifications = prints “No notifications”
    - Some notifications = prints all messages
    '''
    def test_display_notifications_with_messages(self):
        messages = ["Task A due tomorrow", "Task B overdue"]
        output = display_notifications(messages)
        self.assertEqual(output, None, "Expected display_notifications() to print messages without returning a value")
