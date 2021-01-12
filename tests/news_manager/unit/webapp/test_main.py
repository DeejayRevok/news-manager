"""
News manager main tests module
"""
import unittest
from unittest.mock import patch, MagicMock

from aiohttp.web_app import Application
from news_service_lib.config import Configuration

from services.news_service import NewsService
from webapp.main import init_news_manager


class TestMain(unittest.TestCase):
    """
    Main webapp script test cases implementation
    """
    TEST_CONFIG = dict(protocol='test', host='test', port=0)

    # noinspection PyTypeHints
    @patch('webapp.main.initialize_worker')
    @patch('webapp.main.CELERY_APP')
    @patch('webapp.main.NewsPublishService')
    @patch('webapp.main.NewsConsumeService')
    @patch.object(Configuration, 'get')
    @patch('webapp.main.health_check')
    @patch('webapp.main.news_view')
    @patch('webapp.main.storage_factory')
    def test_init_app(self, storage_factory_mock, view_mock, _, config_mock, __, ___, ____, _____):
        """
        Test if the initialization of the app initializes all the required modules
        """
        test_storage_client = MagicMock()
        test_storage_client._mongo_client = MagicMock()
        storage_factory_mock.return_value = test_storage_client
        config_mock.get_section.return_value = self.TEST_CONFIG
        config_mock.get.return_value = 10
        base_app = Application()
        base_app['config'] = config_mock
        app = init_news_manager(base_app)
        view_mock.setup_routes.assert_called_once()
        self.assertIsNotNone(app['news_service'])
        self.assertIsNotNone(app['uaa_service'])
        self.assertTrue(isinstance(app['news_service'], NewsService))
        self.assertIsNotNone(app['uaa_service'])
        self.assertEqual(app['news_service']._client, test_storage_client)


if __name__ == '__main__':
    unittest.main()
