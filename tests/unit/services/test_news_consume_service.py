import json
from dataclasses import asdict
from unittest import TestCase

from news_service_lib.models.named_entity import NamedEntity
from unittest.mock import patch, ANY, Mock

from aiohttp.web_app import Application
from aiounittest import async_test
from dynaconf.loaders import settings_loader
from elasticapm import Client

from news_service_lib.models.new import New
from news_service_lib.nlp_service_service import NlpServiceService

from config import config
from services.news_consume_service import NewsConsumeService
from services.news_service import NewsService
from tests import TEST_CONFIG_PATH
from webapp.container_config import container


class TestNewsConsumeService(TestCase):
    TEST_RABBIT_CONFIG = dict(test="test")
    TEST_NEW = New(
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

    @patch("services.news_consume_service.Process")
    @patch("services.news_consume_service.ExchangeConsumer")
    def setUp(self, consumer_mock, process_mock):
        self.apm_mock = Mock(spec=Client)
        container.reset()
        container.set("apm", self.apm_mock)
        self.consumer_mock = consumer_mock
        self.process_mock = process_mock
        self.news_service_mock = Mock(spec=NewsService)
        self.nlp_service_mock = Mock(spec=NlpServiceService)

        self.app = Application()
        self.consumer_mock.test_connection.return_value = True
        self.news_consume_service = NewsConsumeService(self.news_service_mock, self.nlp_service_mock)

    def test_initialize_consumer(self):
        self.consumer_mock.assert_called_with(
            **self.TEST_RABBIT_CONFIG,
            exchange="news-internal-exchange",
            queue_name="news-exchange",
            message_callback=self.news_consume_service.handle_new,
            logger=ANY,
        )
        self.process_mock.assert_called_with(target=self.consumer_mock().__call__)
        self.assertTrue(self.process_mock().start.called)

    def test_new_update_success(self):
        self.news_service_mock.get_new_by_title.side_effect = KeyError()
        self.news_consume_service.handle_new(None, None, None, json.dumps(asdict(self.TEST_NEW)))
        self.apm_mock.begin_transaction.assert_called_with("consume")
        self.news_service_mock.save_new.assert_called_with(self.TEST_NEW)
        self.apm_mock.end_transaction.assert_called_with("New handle", "OK")

    def test_new_update_fail(self):
        self.news_service_mock.get_new_by_title.side_effect = KeyError()
        self.news_service_mock.save_new.side_effect = Exception("Test")
        self.news_consume_service.handle_new(None, None, None, json.dumps(asdict(self.TEST_NEW)))
        self.apm_mock.end_transaction.assert_called_with("New handle", "FAIL")
        self.apm_mock.capture_exception.assert_called_once()

    @async_test
    async def test_shutdown(self):
        await self.news_consume_service.shutdown()
        self.consumer_mock().shutdown.assert_called_once()
        self.process_mock().join.assert_called_once()
