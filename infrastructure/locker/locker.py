from abc import abstractmethod
from typing import Any, Tuple


class Locker:
    @abstractmethod
    def acquire(self, lock_name: str, blocking: bool = True) -> Tuple[Any, bool]:
        pass

    @abstractmethod
    def release(self, lock_instance: Any):
        pass

    @abstractmethod
    def reset(self):
        pass
