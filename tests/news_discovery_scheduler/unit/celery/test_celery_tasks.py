"""
News discovery celery tasks tests module
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from news_discovery_scheduler.celery_tasks import initialize_worker
from news_service_lib.models import New


class TestCeleryTasks(TestCase):
    """
    News discovery celery tasks tests cases implementation
    """
    TEST_QUEUE_CONFIG = dict(host='test_host', port='0', user='test_user', password='test_password')
    MOCKED_NEW_1 = New(title='Test title 1', url='https://test.test', content='Test content', source='Test source',
                       date=10101010.00)

    MOCKED_NEW_2 = New(title='Test title 2', url='https://test.test', content='Test content', source='Test source',
                       date=10101010.00)

    @patch('news_discovery_scheduler.celery_tasks.DEFINITIONS')
    @patch('news_discovery_scheduler.celery_tasks.PlainCredentials')
    @patch('news_discovery_scheduler.celery_tasks.ConnectionParameters')
    @patch('news_discovery_scheduler.celery_tasks.BlockingConnection')
    @patch('news_discovery_scheduler.celery_tasks.CELERY_APP')
    def test_publish_new(self, _, mocked_connection, __, ___, definitions_mock):
        """
        Test publishing new declares the exchange, publish the new, sets hydrated of new as true, closes the channel
        and closes the connection
        """
        definition_class_mock = MagicMock()
        definition_class_mock().return_value = [self.MOCKED_NEW_1, self.MOCKED_NEW_2]
        definitions_mock.__getitem__.return_value = {'class': definition_class_mock}

        channel_mock = MagicMock()
        mocked_connection().channel.return_value = channel_mock
        initialize_worker()

        from news_discovery_scheduler.celery_tasks import discover_news
        discover_news('test')

        channel_mock.exchange_declare.assert_called_with(exchange='news-internal-exchange', exchange_type='fanout',
                                                         durable=True)
        self.assertEqual(channel_mock.basic_publish.call_count, 2)

        channel_mock.close.assert_called_once()
        mocked_connection().close.assert_called_once()
