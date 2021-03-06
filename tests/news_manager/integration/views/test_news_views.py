"""
News views tests module
"""
import unittest
from time import mktime, strptime
from unittest.mock import patch

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from aiohttp.web_app import Application

from news_service_lib.models.new import New
from services.news_service import NewsService
from webapp.middlewares import error_middleware
from webapp.views.news_view import setup_routes, ROOT_PATH
from webapp.definitions import API_VERSION

MOCKED_RESPONSE = [New(title='Test1', url='https://test.test', content='Test1', source='Test1', date=101001.10),
                   New(title='Test2', url='https://test.test', content='Test2', source='Test2', date=101001.10)]

EXCEPTION_MESSAGE = 'test'


def raise_exception(**_):
    """
    Raise exception helper function
    """
    raise Exception(EXCEPTION_MESSAGE)


async def mock_auth_middleware(_, handler):
    """
    Mocked authentication middleware
    """
    async def middleware(request):
        request.user = {'test': 'test'}
        return await handler(request)

    return middleware


class TestNewsView(AioHTTPTestCase):
    """
    News views test cases implementation
    """
    @patch.object(NewsService, 'get_news_filtered')
    @patch('elasticapm.middleware.ElasticAPM')
    async def get_application(self, mocked_news_service, mock_apm_client):
        """
        Override the get_app method to return your application.
        """

        async def mock_news_response():
            return iter(MOCKED_RESPONSE)

        mocked_news_service.get_news_filtered.return_value = mock_news_response()
        self.mocked_news_service = mocked_news_service
        app = Application()
        app['news_service'] = mocked_news_service
        app['apm'] = mock_apm_client
        app.middlewares.append(error_middleware)
        app.middlewares.append(mock_auth_middleware)
        setup_routes(app)
        return app

    @unittest_run_loop
    async def test_get_news(self):
        """
        Test the get news REST endpoint without params
        """
        resp = await self.client.get(f'/{API_VERSION}{ROOT_PATH}')
        self.assertEqual(resp.status, 200)
        response_content = await resp.json()
        self.assertEqual(response_content[0]['title'], list(MOCKED_RESPONSE)[0].title)
        self.assertEqual(response_content[1]['title'], list(MOCKED_RESPONSE)[1].title)
        self.mocked_news_service.get_news_filtered.assert_called_with(from_date=None, to_date=None)

    @unittest_run_loop
    async def test_get_news_filtered(self):
        """
        Test the get news REST endpoint with query parameters
        """
        query_params = dict(start_date='2019-06-30T20:00:00', end_date='2019-06-30T22:00:00')
        start_parsed = mktime(strptime(query_params['start_date'], '%Y-%m-%dT%H:%M:%S'))
        end_parsed = mktime(strptime(query_params['end_date'], '%Y-%m-%dT%H:%M:%S'))
        resp = await self.client.get(f'/{API_VERSION}{ROOT_PATH}', params=query_params)
        self.assertEqual(resp.status, 200)
        self.mocked_news_service.get_news_filtered.assert_called_with(from_date=start_parsed, to_date=end_parsed)

    @unittest_run_loop
    async def test_get_news_wrong_request(self):
        """
        Test the get news REST endpoint with wrong parameters
        """
        query_params = dict(start_date='WRONG_PARAM', end_date='WRONG_PARAM')
        resp = await self.client.get(f'/{API_VERSION}{ROOT_PATH}', params=query_params)
        self.assertEqual(resp.status, 400)
        self.mocked_news_service.assert_not_called()

    @unittest_run_loop
    async def test_get_news_error(self):
        """
        Test the get news REST endpoint failed
        """
        self.mocked_news_service.get_news_filtered = raise_exception
        self.app['news_service'] = self.mocked_news_service
        resp = await self.client.get(f'/{API_VERSION}{ROOT_PATH}')
        response_content = await resp.json()
        self.assertEqual(resp.status, 500)
        self.assertEqual(response_content['detail'], EXCEPTION_MESSAGE)


if __name__ == '__main__':
    unittest.main()
