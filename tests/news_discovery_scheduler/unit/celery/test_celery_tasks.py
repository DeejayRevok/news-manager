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
    @patch('news_discovery_scheduler.celery_tasks.ExchangePublisher')
    @patch('news_discovery_scheduler.celery_tasks.CELERY_APP')
    def test_discover_news(self, _, publisher_mock, definitions_mock):
        """
        Test discovering the news discover the news and publishes each one of them
        """
        definition_class_mock = MagicMock()
        definition_class_mock().return_value = [self.MOCKED_NEW_1, self.MOCKED_NEW_2]
        definitions_mock.__getitem__.return_value = {'class': definition_class_mock}
        initialize_worker()

        from news_discovery_scheduler.celery_tasks import discover_news
        discover_news('test')

        self.assertEqual(publisher_mock().call_count, 2)
