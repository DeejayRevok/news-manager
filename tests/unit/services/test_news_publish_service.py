from dataclasses import asdict
from unittest import TestCase

from news_service_lib.models.new import New

from news_service_lib.models.named_entity import NamedEntity
from unittest.mock import patch, call, ANY, Mock, MagicMock

from aiohttp.web_app import Application
from aiounittest import async_test
from dynaconf.loaders import settings_loader

from infrastructure.locker import Locker

from config import config
from services.news_publish_service import NewsPublishService
from services.news_service import NewsService
from tests import TEST_CONFIG_PATH


class TestNewsPublishService(TestCase):
    TEST_RABBIT_CONFIG = dict(test="test")
    TEST_NEW_INSERT_CHANGE = New(
        title="test_title",
        url="https://test.test",
        content="test_content",
        date=12313.0,
        language="test_language",
        source="test_source",
        entities=[NamedEntity(text="test_named_entity_text", type="test_named_entity_type")],
    )

    @classmethod
    def setUpClass(cls) -> None:
        settings_loader(config, filename=TEST_CONFIG_PATH)
        config.rabbit = cls.TEST_RABBIT_CONFIG

    @patch("services.news_publish_service.Process")
    @patch("services.news_publish_service.ExchangePublisher")
    def setUp(self, publisher_mock, process_mock):
        self.locker_client_mock = Mock(spec=Locker)
        self.publisher_mock = publisher_mock
        self.process_mock = process_mock
        self.news_service_mock = Mock(spec=NewsService)
        self.news_service_mock.consume_new_inserts.return_value = [
            ("test", self.TEST_NEW_INSERT_CHANGE),
            ("test", self.TEST_NEW_INSERT_CHANGE),
        ]
        self.app = Application()
        self.publisher_mock.test_connection.return_value = True
        self.news_publish_service = NewsPublishService(self.news_service_mock, self.locker_client_mock)

    def test_initialize_publisher(self):
        self.publisher_mock.assert_called_with(**self.TEST_RABBIT_CONFIG, exchange="news", logger=ANY)
        self.process_mock.assert_called_with(target=self.news_publish_service.__call__)
        self.assertTrue(self.process_mock().start.called)

    def test_call_publish_service(self):
        self.locker_client_mock.acquire.return_value = (MagicMock(), True)

        self.news_publish_service()
        self.publisher_mock().connect.assert_called_once()
        self.publisher_mock().initialize.assert_called_once()
        self.publisher_mock().assert_called_with(asdict(self.TEST_NEW_INSERT_CHANGE))
        call_calls = self.publisher_mock().mock_calls.count(call(asdict(self.TEST_NEW_INSERT_CHANGE)))
        self.assertEqual(call_calls, 2)

    @async_test
    async def test_shutdown(self):
        await self.news_publish_service.shutdown()
        self.publisher_mock().shutdown.assert_called_once()
        self.process_mock().join.assert_called_once()
