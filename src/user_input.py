"""
Author: Foo Enn Qi
Custom Project: Smart Task Manager (STM)
FIT2107 Software Quality and Testing

Reusable input-handling and validation functions.
"""

from datetime import date


# --------------------------
# Generic Validators
# --------------------------

def is_int(val) -> bool:
    """Verify if a value is a valid integer."""
    try:
        int(val)
        return True
    except ValueError:
        return False


def read_string(prompt: str) -> str:
    """Read a non-empty string from the user."""
    line = input(prompt).strip()
    while not line:
        print("[!] Input cannot be empty.")
        line = input(prompt).strip()
    return line


def read_integer_range(prompt: str, min_val: int, max_val: int) -> int:
    """Read an integer within a specific range."""
    while True:
        val = input(prompt).strip()
        if not is_int(val):
            print("[!] Please enter a valid integer.")
            continue
        num = int(val)
        if num < min_val or num > max_val:
            print(f"[!] Please enter a number between {min_val} and {max_val}.")
        else:
            return num


# --------------------------
# STM-Specific Input Helpers
# --------------------------

def read_task_name(prompt: str = "Enter task name: ") -> str:
    """Ask user for a task name and ensure it's not empty."""
    return read_string(prompt)


def read_category() -> str:
    """Ask user to select a valid category from four options."""
    categories = ["Work", "Personal", "Study", "Health"]
    print("\nSelect Task Category:")
    for i, cat in enumerate(categories, start=1):
        print(f"  {i}. {cat}")

    choice = read_integer_range("Enter your choice (1–4): ", 1, 4)
    return categories[choice - 1]


def read_priority() -> str:
    """Ask user to select a valid priority level."""
    priorities = ["High", "Medium", "Low"]
    print("\nSelect Task Priority:")
    for i, p in enumerate(priorities, start=1):
        print(f"  {i}. {p}")

    choice = read_integer_range("Enter your choice (1–3): ", 1, 3)
    return priorities[choice - 1]


def read_deadline(allow_past: bool = False, prompt: str = "Enter task deadline (YYYY-MM-DD): ") -> str:
    """
    Prompt the user for a valid date (YYYY-MM-DD).
    If allow_past is False, the date must be today or in the future.
    """
    today = date.today()
    while True:
        deadline_str = input(prompt).strip()
        try:
            y, m, d = map(int, deadline_str.split("-"))
            candidate = date(y, m, d)
            if not allow_past and candidate < today:
                print(f"[!] Deadline cannot be in the past. Today is {today}. Please enter today or a future date.")
                continue
            return deadline_str
        except ValueError:
            print("[!] Invalid date format. Please try again (YYYY-MM-DD).")


# --------------
# Add Task flow
# --------------

def read_yes_no(prompt: str = "Is this okay? (y/n): ") -> bool:
    """Read a yes/no answer and return True/False."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("[!] Please answer with 'y' or 'n'.")

def read_recurrence_type() -> str:
    """
    Ask user for recurrence type.
    Returns one of: 'daily', 'weekly', 'monthly'.
    """
    print("\nSelect Recurrence Type:")
    options = ["daily", "weekly", "monthly"]
    for i, opt in enumerate(options, start=1):
        print(f"  {i}. {opt.capitalize()}")
    choice = read_integer_range("Enter your choice (1–3): ", 1, 3)
    return options[choice - 1]
