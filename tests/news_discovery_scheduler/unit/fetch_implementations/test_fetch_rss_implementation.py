"""
Fetch RSS implementation tests module
"""
from unittest import TestCase
from unittest.mock import MagicMock

from news_discovery_scheduler.discovery.fetch_implementations.fetch_rss_news_implementation import \
    FetchRssNewsImplementation


class TestFetchRSSImplementation(TestCase):
    """
    Fetch RSS implementation test cases implementation
    """
    def test_fetch(self):
        """
        Test calling the fetch rss implementation yields from the source adapters
        """
        source_adapter_1 = MagicMock()
        source_adapter_2 = MagicMock()
        test_definition = dict(source_adapters=[source_adapter_1, source_adapter_2])
        list(FetchRssNewsImplementation(test_definition)())
        source_adapter_1().fetch.assert_called_once()
        source_adapter_2().fetch.assert_called_once()
