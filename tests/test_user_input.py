import unittest
from unittest.mock import patch
from src.user_input import (
    is_int, read_string, read_integer_range,
    read_task_name, read_category, read_priority, read_yes_no
)

class TestUserInput(unittest.TestCase):

    # --- is_int() --------
    '''
    EP:
    - Valid integer strings = True
    - Invalid (non-numeric or float) = False
    '''
    def test_is_int_positive_number(self):
        self.assertTrue(is_int("123"), "Expected '123' to be recognized as valid integer")

    def test_is_int_negative_number(self):
        self.assertTrue(is_int("-456"), "Expected '-456' to be recognized as valid integer")

    def test_is_int_alphabetic_string(self):
        self.assertFalse(is_int("abc"), "Expected 'abc' to be invalid integer string")

    def test_is_int_float_string(self):
        self.assertFalse(is_int("12.34"), "Expected '12.34' to be invalid integer string")

    # --- read_string() ----------
    '''
    EP + Mocking:
    - Empty input = re-prompt
    - Non-empty input = accepted
    '''
    @patch("builtins.input", side_effect=["", "valid input"])
    def test_read_string_empty_then_valid(self, mock_input):
        result = read_string("Enter: ")
        self.assertEqual(result, "valid input", "Expected re-prompt and accept 'valid input' after empty input")

    @patch("builtins.input", return_value="test string")
    def test_read_string_valid(self, mock_input):
        result = read_string("Enter: ")
        self.assertEqual(result, "test string", "Expected valid non-empty input to be accepted immediately")

    # --- read_integer_range() -------
    '''
    BVA + EP:
    - Invalid input (non-integer, out of range) = re-prompt
    - Valid integer within range = accepted
    '''
    @patch("builtins.input", side_effect=["abc", "0", "2"])
    def test_read_integer_range_invalid_then_valid(self, mock_input):
        result = read_integer_range("Enter (1-3): ", 1, 3)
        self.assertEqual(result, 2, "Expected valid integer '2' after rejecting 'abc' and '0'")

    @patch("builtins.input", return_value="2")
    def test_read_integer_range_valid(self, mock_input):
        result = read_integer_range("Enter (1-3): ", 1, 3)
        self.assertEqual(result, 2, "Expected valid integer '2' within range to be accepted")

    # --- read_task_name() ----------
    '''
    EP:
    - Valid non-empty task name accepted
    '''
    @patch("builtins.input", return_value="My Task")
    def test_read_task_name_valid(self, mock_input):
        result = read_task_name()
        self.assertEqual(result, "My Task", "Expected task name 'My Task' to be accepted")

    # --- read_category() ------
    '''
    EP:
    - User selects category by index = correct category returned
    '''
    @patch("builtins.input", return_value="2")
    def test_read_category_personal(self, mock_input):
        result = read_category()
        self.assertEqual(result, "Personal", "Expected category 'Personal' for input '2'")

    # --- read_priority() ------
    '''
    EP:
    - User selects priority by index = correct priority returned
    '''
    @patch("builtins.input", return_value="1")
    def test_read_priority_high(self, mock_input):
        result = read_priority()
        self.assertEqual(result, "High", "Expected priority 'High' for input '1'")

    # --- read_yes_no() -------
    '''
    EP + Mocking:
    - Invalid = re-prompt
    - 'y' = True
    - 'n' = False
    '''
    @patch("builtins.input", side_effect=["maybe", "y"])
    def test_read_yes_no_invalid_then_yes(self, mock_input):
        result = read_yes_no("Continue? ")
        self.assertTrue(result, "Expected True after rejecting invalid input 'maybe' and accepting 'y'")

    @patch("builtins.input", return_value="n")
    def test_read_yes_no_no(self, mock_input):
        result = read_yes_no("Continue? ")
        self.assertFalse(result, "Expected False for input 'n'")
