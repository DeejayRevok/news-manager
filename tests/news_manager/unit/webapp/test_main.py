"""
News manager main tests module
"""
import unittest
from unittest.mock import patch, MagicMock

from aiohttp.web_app import Application
from dynaconf.loaders import settings_loader

from config import config
from services.news_service import NewsService
from tests import TEST_CONFIG_PATH
from webapp.main import init_news_manager


class TestMain(unittest.TestCase):
    """
    Main webapp script test cases implementation
    """

    # noinspection PyTypeHints
    @patch('webapp.main.NlpServiceService')
    @patch('webapp.main.locker_factory')
    @patch('webapp.main.NewsPublishService')
    @patch('webapp.main.NewsConsumeService')
    @patch('webapp.main.health_check')
    @patch('webapp.main.news_view')
    @patch('webapp.main.storage_factory')
    def test_init_app(self, storage_factory_mock, view_mock, _, __, ___, ____, _____):
        """
        Test if the initialization of the app initializes all the required modules
        """
        settings_loader(config, filename=TEST_CONFIG_PATH)
        test_storage_client = MagicMock()
        test_storage_client._mongo_client = MagicMock()
        storage_factory_mock.return_value = test_storage_client
        base_app = Application()
        app = init_news_manager(base_app)
        view_mock.setup_routes.assert_called_once()
        self.assertIsNotNone(app['news_service'])
        self.assertIsNotNone(app['uaa_service'])
        self.assertTrue(isinstance(app['news_service'], NewsService))
        self.assertIsNotNone(app['uaa_service'])
        self.assertEqual(app['news_service']._client, test_storage_client)


if __name__ == '__main__':
    unittest.main()
