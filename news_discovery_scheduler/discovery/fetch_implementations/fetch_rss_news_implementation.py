"""
Fetch news discovery module
"""
from typing import Iterator

from news_service_lib.models import New

from news_discovery_scheduler.discovery.fetch_implementations.fetch_implementation import FetchImplementation
from log_config import get_logger

LOGGER = get_logger()


class FetchRssNewsImplementation(FetchImplementation):
    """
    Fetch news from rss discovery implementation
    """
    def __init__(self, definition: dict):
        """
        Initialize the fetch news discovery

        Args:
            definition: fetch news discovery definition parameters
        """
        FetchImplementation.__init__(self, definition)

    def __call__(self) -> Iterator[New]:
        """
        Fetch news from rss functionality
        """
        for adapter_class in self.definition['source_adapters']:
            adapter = adapter_class(self.definition)
            yield from adapter.fetch()
