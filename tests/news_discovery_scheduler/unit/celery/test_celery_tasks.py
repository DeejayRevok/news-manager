"""
News discovery celery tasks tests module
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from dynaconf.loaders import settings_loader

from news_discovery_scheduler.container_config import container
from news_discovery_scheduler.discovery.fetch_implementations.fetch_implementation import FetchImplementation
from news_service_lib.messaging import ExchangePublisher
from news_service_lib.models import New

from config import config
from tests import TEST_CONFIG_PATH


class TestCeleryTasks(TestCase):
    """
    News discovery celery tasks tests cases implementation
    """
    TEST_QUEUE_CONFIG = dict(host='test_host', port='0', user='test_user', password='test_password')
    MOCKED_NEW_1 = New(title='Test title 1', url='https://test.test', content='Test content', source='Test source',
                       date=10101010.00)

    MOCKED_NEW_2 = New(title='Test title 2', url='https://test.test', content='Test content', source='Test source',
                       date=10101010.00)

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initialize the test case environment
        """
        container.reset()
        settings_loader(config, filename=TEST_CONFIG_PATH)
        config.rabbit = cls.TEST_QUEUE_CONFIG
        cls.exchange_publisher_mock = Mock(spec=ExchangePublisher)
        container.set('exchange_publisher', cls.exchange_publisher_mock)

    @patch('news_discovery_scheduler.celery_tasks.CELERY_APP')
    @patch('news_discovery_scheduler.celery_tasks.DEFINITIONS')
    def test_discover_news(self, definitions_mock, _):
        """
        Test discover news publish the discovered news
        """
        definition_class_mock = Mock(spec=FetchImplementation)
        definition_class_mock().return_value = [self.MOCKED_NEW_1, self.MOCKED_NEW_2]
        definitions_mock.__getitem__.return_value = {'class': definition_class_mock}

        from news_discovery_scheduler.celery_tasks import discover_news
        discover_news('test')

        self.assertEqual(self.exchange_publisher_mock.call_count, 2)
