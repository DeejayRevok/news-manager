"""
Celery beat tests module
"""
from unittest import TestCase
from unittest.mock import patch, MagicMock

from news_discovery_scheduler.celery_beat import setup_periodic_tasks
from news_discovery_scheduler.discovery.definitions import DEFINITIONS


class TestCeleryBeat(TestCase):
    """
    Celery beat test cases implementation
    """
    @patch('news_discovery_scheduler.celery_beat.BaseCeleryApp')
    def test_setup_periodic_tasks(self, _):
        """
        Test setting up the periodic tasks add one periodic task for each definition
        """
        sender_mock = MagicMock()
        setup_periodic_tasks(sender_mock)

        self.assertEqual(len(DEFINITIONS), sender_mock.add_periodic_task.call_count)
