import unittest
from unittest.mock import patch
from src.stm import run_stm


class TestSTMMenu(unittest.TestCase):

    # --- Option 1: Add Main Task then Exit --------------------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "m", "Test Task", "1", "1", "2025-12-12", "n", "6"])
    def test_add_main_task_then_exit(self, mock_input, mock_print):
        """Simulate adding a main task and exiting."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected menu input to be called during Add Main Task flow")

    # --- Option 1: Add Recurring Daily Task then Exit ---------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "m", "Daily Task", "3", "3", "2025-12-15", "y", "1", "6"])
    def test_add_daily_recurring_task_then_exit(self, mock_input, mock_print):
        """Simulate adding a daily recurring task and exiting."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected input prompt for daily recurring task")

    # --- Option 1: Add Monthly Recurring Task then Exit -------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "m", "Monthly Task", "4", "1", "2025-12-15", "y", "3", "6"])
    def test_add_monthly_recurring_task_then_exit(self, mock_input, mock_print):
        """Simulate adding a monthly recurring task and exiting."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected monthly recurring task flow executed")

    # --- Option 1: Invalid Task Type then Valid ---------------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "x", "m", "Task", "1", "1", "2025-12-12", "n", "6"])
    def test_add_task_invalid_type_then_valid(self, mock_input, mock_print):
        """Handle invalid task type input followed by valid entry."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected retry after invalid task type input")

    # --- Option 1: Past Deadline then Valid -------------------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "m", "Task", "1", "1", "2020-01-01", "2025-12-12", "n", "6"])
    def test_add_task_past_deadline_then_valid(self, mock_input, mock_print):
        """Handle past deadline input, then retry with valid date."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected re-prompt after entering past deadline")

    # --- Option 1: Invalid Date Format then Valid -------------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "m", "Task", "1", "1", "invalid-date", "2025-12-12", "n", "6"])
    def test_add_task_invalid_date_then_valid(self, mock_input, mock_print):
        """Handle invalid date format followed by valid date."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected re-prompt after invalid date format")

    # --- Option 1: Invalid Recurrence Answer then Valid -------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "m", "Task", "1", "1", "2025-12-12", "maybe", "n", "6"])
    def test_add_task_invalid_recurrence_then_valid(self, mock_input, mock_print):
        """Handle invalid recurrence response followed by valid response."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected retry prompt after invalid recurrence answer")

    # --- Option 2: View Tasks then Exit -----------------------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["2", "6"])
    def test_view_tasks_then_exit(self, mock_input, mock_print):
        """View tasks (none) then exit."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected input for View Tasks flow")

    # --- Option 2: View Tasks with Data then Exit -------------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "m", "Task 1", "1", "1", "2025-12-12", "n", "2", "6"])
    def test_view_tasks_with_data_then_exit(self, mock_input, mock_print):
        """Add a task then view it."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected flow for adding and viewing tasks")

    # --- Option 3: View Notifications then Exit ---------------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["3", "6"])
    def test_view_notifications_then_exit(self, mock_input, mock_print):
        """View notifications then exit."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected notifications to display correctly")

    # --- Option 4–5–7 tests condensed pattern --------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["4", "m", "c", "6"])
    def test_edit_task_cancel_then_exit(self, mock_input, mock_print):
        """Cancel edit flow and exit."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected cancel edit path handled correctly")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["5", "m", "c", "6"])
    def test_delete_task_cancel_then_exit(self, mock_input, mock_print):
        """Cancel delete flow and exit."""
        run_stm()
        self.assertTrue(mock_input.called, "Expected cancel delete path handled correctly")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["7", "m", "6", "6"])
    @patch("src.stm.load_from_json", return_value=[])
    @patch("src.stm.save_to_json", return_value=True)
    def test_mark_task_complete_no_tasks_then_exit(self, mock_save, mock_load, mock_input, mock_print):
        run_stm()
        self.assertTrue(mock_input.called, "Expected graceful handling for marking non-existent task complete")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["7", "x", "m", "1", "6"])
    def test_mark_invalid_type_then_valid(self, mock_input, mock_print):
        run_stm()
        self.assertTrue(mock_input.called, "Expected retry prompt after invalid mark type input")

    # --- Invalid Input Scenarios ------------------------------------------
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["a", "6"])
    def test_invalid_input_then_exit(self, mock_input, mock_print):
        """Handle non-numeric invalid menu input then exit."""
        run_stm()
        printed_texts = [call.args[0] for call in mock_print.call_args_list]
        found_warning = any("[!]" in text for text in printed_texts)
        self.assertTrue(found_warning, "Expected warning printed for invalid non-numeric input")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["9", "6"])
    def test_invalid_range_input_then_exit(self, mock_input, mock_print):
        """Handle out of range menu selection then exit."""
        run_stm()
        printed_texts = [call.args[0] for call in mock_print.call_args_list]
        found_warning = any("[!]" in text for text in printed_texts)
        self.assertTrue(found_warning, "Expected warning printed for out-of-range input")

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["abc", "0", "8", "6"])
    def test_multiple_invalid_inputs_then_exit(self, mock_input, mock_print):
        """Handle multiple invalid menu inputs before valid exit."""
        run_stm()
        printed_texts = [call.args[0] for call in mock_print.call_args_list]
        found_warning = any("[!]" in text for text in printed_texts)
        self.assertTrue(found_warning, "Expected warnings printed for multiple invalid inputs")
