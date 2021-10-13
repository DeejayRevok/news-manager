from logging import getLogger

import unittest
from time import mktime, strptime
from unittest.mock import Mock

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from aiohttp.web_app import Application
from elasticapm import Client

from news_service_lib.models.new import New
from services.news_service import NewsService
from webapp.container_config import container
from webapp.middlewares import error_middleware
from webapp.definitions import API_VERSION
from webapp.views.news_view import NewsView

MOCKED_RESPONSE = [
    New(
        title="Test1",
        url="https://test.test",
        content="Test1",
        source="Test1",
        date=101001.10,
        language="test_language",
    ),
    New(
        title="Test2",
        url="https://test.test",
        content="Test2",
        source="Test2",
        date=101001.10,
        language="test_language",
    ),
]


async def mock_auth_middleware(_, handler):
    async def middleware(request):
        request.user = {"test": "test"}
        return await handler(request)

    return middleware


class TestNewsView(AioHTTPTestCase):
    async def get_application(self):
        container.reset()
        container.set("apm", Mock(spec=Client))
        self.mocked_news_service = Mock(spec=NewsService)

        app = Application()
        app.middlewares.append(error_middleware)
        app.middlewares.append(mock_auth_middleware)
        NewsView(app, self.mocked_news_service, getLogger())
        return app

    @unittest_run_loop
    async def test_get_news(self):
        self.mocked_news_service.get_news_filtered.return_value = iter(MOCKED_RESPONSE)
        resp = await self.client.get(f"/{API_VERSION}/api/news")
        self.assertEqual(resp.status, 200)
        response_content = await resp.json()
        self.assertEqual(response_content[0]["title"], list(MOCKED_RESPONSE)[0].title)
        self.assertEqual(response_content[1]["title"], list(MOCKED_RESPONSE)[1].title)
        self.mocked_news_service.get_news_filtered.assert_called_with(from_date=None, to_date=None)

    @unittest_run_loop
    async def test_get_news_filtered(self):
        self.mocked_news_service.get_news_filtered.return_value = iter(MOCKED_RESPONSE)

        query_params = dict(start_date="2019-06-30T20:00:00", end_date="2019-06-30T22:00:00")
        start_parsed = mktime(strptime(query_params["start_date"], "%Y-%m-%dT%H:%M:%S"))
        end_parsed = mktime(strptime(query_params["end_date"], "%Y-%m-%dT%H:%M:%S"))
        resp = await self.client.get(f"/{API_VERSION}/api/news", params=query_params)
        self.assertEqual(resp.status, 200)
        self.mocked_news_service.get_news_filtered.assert_called_with(from_date=start_parsed, to_date=end_parsed)

    @unittest_run_loop
    async def test_get_news_wrong_request(self):
        query_params = dict(start_date="WRONG_PARAM", end_date="WRONG_PARAM")
        resp = await self.client.get(f"/{API_VERSION}/api/news", params=query_params)
        self.assertEqual(resp.status, 400)
        self.mocked_news_service.assert_not_called()

    @unittest_run_loop
    async def test_get_news_error(self):
        exception_message = "test"
        self.mocked_news_service.get_news_filtered.side_effect = Exception(exception_message)
        resp = await self.client.get(f"/{API_VERSION}/api/news")
        response_content = await resp.json()
        self.assertEqual(resp.status, 500)
        self.assertEqual(response_content["detail"], exception_message)


if __name__ == "__main__":
    unittest.main()
