"""
Factories tests module
"""
import unittest
from unittest.mock import patch, Mock

from cron.cron_factory import initialize_crons


class DummyImplementation:
    """
    Cron dummy implementation helper
    """
    def __init__(self, dummy_app, definition):
        self.app = dummy_app
        self.definition = definition
        dummy_app()


class TestFactories(unittest.TestCase):
    """
    Factories test cases
    """

    @patch('discovery.cron_factory.DEFINITIONS')
    def test_initialize_crons(self, mocked_definitions):
        """
        Test the correct initialization of the defined crons
        """
        definitions_dummy = {
            'definition_1': {
                'class': DummyImplementation
            },
            'definition_2': {
                'class': DummyImplementation
            }
        }
        mocked_definitions.values.return_value = definitions_dummy.values()
        mock_app = Mock()
        initialize_crons(mock_app)
        self.assertEqual(mock_app.call_count, 2)


if __name__ == '__main__':
    unittest.main()
