"""
News manager main tests module
"""
import unittest
from unittest.mock import patch

from aiohttp.web_app import Application
from dynaconf.loaders import settings_loader

from config import config
from tests import TEST_CONFIG_PATH
from webapp.main import init_news_manager


class TestMain(unittest.TestCase):
    """
    Main webapp script test cases implementation
    """

    @patch('webapp.main.container')
    @patch('webapp.main.health_check')
    @patch('webapp.main.load')
    @patch('webapp.main.setup_graphql_routes')
    @patch('webapp.main.news_view')
    def test_init_app(self, view_mock, setup_graphql_mock, load_mock, *_):
        """
        Test if the initialization of the app initializes all the required modules
        """
        settings_loader(config, filename=TEST_CONFIG_PATH)
        base_app = Application()
        init_news_manager(base_app)
        view_mock.setup_routes.assert_called_once()
        setup_graphql_mock.assert_called_once()
        load_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
