from datetime import datetime
from logging import Logger
from unittest import TestCase
from unittest.mock import Mock

from application.get_news.get_news_query import GetNewsQuery
from application.get_news.get_news_query_handler import GetNewsQueryHandler
from domain.new.find_news_criteria import FindNewsCriteria
from domain.new.new import New
from domain.new.new_repository import NewRepository


class TestGetNewsQueryHandler(TestCase):
    def setUp(self) -> None:
        self.new_repository_mock = Mock(spec=NewRepository)
        self.logger = Mock(spec=Logger)
        self.query_handler = GetNewsQueryHandler(
            self.new_repository_mock,
            self.logger
        )

    def test_handle_success(self):
        test_query = GetNewsQuery(
            source="test_source",
            hydrated=True,
            from_sentiment=2.0,
            to_sentiment=10.0,
            from_date="2022-12-22",
            to_date="2022-12-30",
        )
        test_new = New(
            title="test_title",
            url="test_url",
            content="test_content",
            source="test_source",
            date=2341231.23,
            language="test_language",
            hydrated=True
        )
        self.new_repository_mock.find_by_criteria.return_value = [test_new, test_new]

        query_response = self.query_handler.handle(test_query)

        self.assertEqual([test_new, test_new], query_response.data)
        expected_from_date = datetime.fromisoformat("2022-12-22").timestamp()
        expected_to_date = datetime.fromisoformat("2022-12-30").timestamp()
        self.new_repository_mock.find_by_criteria.assert_called_once_with(
            FindNewsCriteria(
                source="test_source",
                hydrated=True,
                from_sentiment=2.0,
                to_sentiment=10.0,
                from_date=expected_from_date,
                to_date=expected_to_date,
            )
        )
