import asyncio
from unittest import TestCase
from unittest.mock import Mock

from aiohttp.abc import Request
from graphene.test import Client
from graphql.execution.executors.asyncio import AsyncioExecutor
from news_service_lib.models.new import New
from services.news_service import NewsService
from webapp.container_config import container

from webapp.graph import schema


class TestNewsQueries(TestCase):
    TEST_NEW = New(
        title="Test1",
        url="https://test.test",
        content="Test1",
        source="Test1",
        date=101001.10,
        language="test_language",
    )
    TEST_ANOTHER_NEW = New(
        title="Test2",
        url="https://test.test",
        content="Test2",
        source="Test2",
        date=101001.10,
        language="test_language",
    )

    def setUp(self) -> None:
        container.reset()
        self.news_service_mock = Mock(spec=NewsService)
        container.set("news_service", self.news_service_mock)

    def test_get_new_title(self):
        self.news_service_mock.get_new_by_title.return_value = self.TEST_NEW
        request_mock = Mock(spec=Request)
        request_mock.user = True

        client = Client(schema)
        executed = client.execute(
            """{ 
                                        new(title: "test_query_title"){
                                            title
                                        }
                                      }""",
            context_value=dict(request=request_mock),
            executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
        )

        self.news_service_mock.get_new_by_title.assert_called_with("test_query_title")
        expected_data = dict(new=dict(title=self.TEST_NEW.title))
        self.assertEqual(executed["data"], expected_data)

    def test_get_news(self):
        self.news_service_mock.get_news_filtered.return_value = [self.TEST_NEW, self.TEST_ANOTHER_NEW]
        request_mock = Mock(spec=Request)
        request_mock.user = True

        client = Client(schema)
        executed = client.execute(
            """{ 
                                        news(source: "test_source"){
                                            title
                                        }
                                      }""",
            context_value=dict(request=request_mock),
            executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
        )

        self.news_service_mock.get_news_filtered.assert_called_with(
            from_date=None, hydration=None, sentiment=(None, True), source="test_source", to_date=None
        )

        expected_data = dict(news=[dict(title=self.TEST_NEW.title), dict(title=self.TEST_ANOTHER_NEW.title)])
        self.assertEqual(executed["data"], expected_data)
