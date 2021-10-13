import asyncio
import unittest
from dataclasses import asdict
from unittest.mock import patch, Mock

from infrastructure.storage.filter.range_filter import RangeFilter
from infrastructure.storage.mongo_sort_direction import MongoSortDirection
from infrastructure.storage.mongo_storage_client import MongoStorageClient
from news_service_lib.models.new import New
from services.news_service import NewsService

MOCKED_NEW = New(
    title="Test title",
    url="https://test.test",
    content="Test content",
    source="Test source",
    language="test_language",
    date=10101010.00,
)


class TestNewsService(unittest.TestCase):
    def test_save_new(self):
        storage_client_mock = Mock(spec=MongoStorageClient)
        storage_client_mock.get_one.return_value = {"_id": "test_id"}
        news_service = NewsService(storage_client_mock)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(news_service.save_new(MOCKED_NEW))

        storage_client_mock.save.assert_called_with(asdict(MOCKED_NEW))

    def test_get_news_empty(self):
        storage_client_mock = Mock(spec=MongoStorageClient)
        news_service = NewsService(storage_client_mock)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(news_service.get_news_filtered())

        storage_client_mock.get.assert_called()

    def test_get_news_date_range(self):
        storage_client_mock = Mock(spec=MongoStorageClient)
        news_service = NewsService(storage_client_mock)
        start = 1
        end = 2

        loop = asyncio.new_event_loop()
        loop.run_until_complete(news_service.get_news_filtered(from_date=start, to_date=end))

        storage_client_mock.get.assert_called_with(
            [RangeFilter("date", upper=end, lower=start)], sort_key="date", sort_direction=MongoSortDirection.DESC
        )

        loop = asyncio.new_event_loop()
        loop.run_until_complete(news_service.get_news_filtered(from_date=start))

        storage_client_mock.get.assert_called_with(
            [RangeFilter("date", upper=None, lower=start)], sort_key="date", sort_direction=MongoSortDirection.DESC
        )

        loop = asyncio.new_event_loop()
        loop.run_until_complete(news_service.get_news_filtered(to_date=end))

        storage_client_mock.get.assert_called_with(
            [RangeFilter("date", upper=end, lower=None)], sort_key="date", sort_direction=MongoSortDirection.DESC
        )


if __name__ == "__main__":
    unittest.main()
