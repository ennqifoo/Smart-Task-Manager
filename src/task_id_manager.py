"""
task_id_manager.py
------------------
Handles unique Task ID generation and reset logic.
Designed as a singleton to ensure global consistency.
"""

class TaskIDManager:
    """Manages task ID generation without global variables."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.counter = 0
        return cls._instance

    def next_id(self) -> int:
        """Generate unique, auto-incrementing Task ID."""
        self.counter += 1
        return self.counter

    def reset_for_tests(self) -> None:
        """Reset task ID counter for testing consistency."""
        self.counter = 0

    def update_seed(self, seed: int) -> None:
        """
        Ensure future auto IDs are greater than any existing ID.
        Example: if you pass 12, the next auto ID will be 13.
        """
        if seed > self.counter:
            self.counter = seed


# Global singleton instance
_id_manager = TaskIDManager()


def next_task_id() -> int:
    """Public function to get next unique Task ID."""
    return _id_manager.next_id()


def reset_task_id_for_tests() -> None:
    """Reset counter for testing consistency."""
    _id_manager.reset_for_tests()


def update_task_id_seed(seed: int) -> None:
    """Ensure future IDs are greater than existing ones."""
    _id_manager.update_seed(seed)
