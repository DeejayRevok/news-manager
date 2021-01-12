"""
Generic discovery runner and interface module
"""
from abc import abstractmethod
from typing import Iterator

from news_service_lib.models import New


class FetchImplementation:
    """
    Generic discovery runner implementation
    """
    def __init__(self, definition: dict):
        """
        Initialize the discovery runner

        Args:
            definition: specific discovery definition params
        """
        self.definition = definition

    @abstractmethod
    def __call__(self) -> Iterator[New]:
        """
        Specific discovery functionality
        """
