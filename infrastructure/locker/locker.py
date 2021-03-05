"""
Locker definition module
"""
from abc import abstractmethod
from typing import Any, Tuple


class Locker:
    """
    Locker abstract class implementation
    """
    @abstractmethod
    def acquire(self, lock_name: str, blocking: bool = True) -> Tuple[Any, bool]:
        """
        Acquire a lock identified by the given name waiting until it is not blocked if "blocking"

        Args:
            lock_name: name of the lock to acquire
            blocking: True if the lock should be awaited if it is already blocked, False otherwise

        Returns: lock instance and True if the lock is acquired, False otherwise

        """

    @abstractmethod
    def release(self, lock_instance: Any):
        """
        Release the provided lock

        Args:
            lock_instance: lock to release

        """

    @abstractmethod
    def reset(self):
        """
        Reset and clear the locker
        """
