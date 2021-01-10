"""
Generic cron runner and interface module
"""
from abc import abstractmethod
from typing import Iterator

from news_service_lib.models import New


class FetchImplementation:
    """
    Generic cron runner implementation
    """
    def __init__(self, definition: dict):
        """
        Initialize the cron runner

        Args:
            definition: specific cron definition params
        """
        self.definition = definition

    @abstractmethod
    def __call__(self) -> Iterator[New]:
        """
        Specific cron functionality
        """
