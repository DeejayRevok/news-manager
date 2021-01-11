"""
News discovery celery tasks tests module
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from news_service_lib.models import New


class TestCeleryTasks(TestCase):
    """
    News discovery celery tasks tests cases implementation
    """
    MOCKED_NEW_1 = New(title='Test title 1', url='https://test.test', content='Test content', source='Test source',
                       date=10101010.00)

    MOCKED_NEW_2 = New(title='Test title 2', url='https://test.test', content='Test content', source='Test source',
                       date=10101010.00)

    @patch('news_discovery_scheduler.celery_tasks.DEFINITIONS')
    @patch('news_discovery_scheduler.celery_tasks.Exchange')
    @patch('news_discovery_scheduler.celery_tasks.CELERY_APP')
    def test_discover_news(self, _, exchange_mock, definitions_mock):
        """
        Test the discover news task fetches news from the definition specified and publish the news
        """
        definition_class_mock = MagicMock()
        definition_class_mock().return_value = [self.MOCKED_NEW_1, self.MOCKED_NEW_2]
        definitions_mock.__getitem__.return_value = {'class': definition_class_mock}

        from news_discovery_scheduler.celery_tasks import discover_news
        discover_news('test')

        self.assertEqual(exchange_mock().publish.call_count, 2)
