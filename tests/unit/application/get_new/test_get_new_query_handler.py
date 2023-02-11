from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from domain.new.new_not_found_exception import NewNotFoundException

from application.get_new.get_new_query import GetNewQuery

from application.get_new.get_new_query_handler import GetNewQueryHandler
from domain.new.new import New
from domain.new.new_repository import NewRepository


class TestGetNewQueryHandler(TestCase):
    def setUp(self) -> None:
        self.new_repository_mock = Mock(spec=NewRepository)
        self.logger_mock = Mock(spec=Logger)
        self.query_handler = GetNewQueryHandler(self.new_repository_mock, self.logger_mock)

    def test_handle_success(self):
        test_new = New(
            title="test_title",
            url="test_url",
            content="test_content",
            source="test_source",
            date=2341231.23,
            language="test_language",
            hydrated=True,
        )
        self.new_repository_mock.find_by_title.return_value = test_new
        test_query = GetNewQuery(title="test_title")

        query_response = self.query_handler.handle(test_query)

        self.assertEqual(test_new, query_response.data)
        self.new_repository_mock.find_by_title.assert_called_once_with("test_title")

    def test_handle_not_found(self):
        self.new_repository_mock.find_by_title.return_value = None
        test_query = GetNewQuery(title="test_title")

        with self.assertRaises(NewNotFoundException) as context:
            self.query_handler.handle(test_query)

        self.assertEqual("test_title", context.exception.title)
        self.new_repository_mock.find_by_title.assert_called_once_with("test_title")
