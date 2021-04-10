"""
Middlewares tests module
"""
from unittest import TestCase
from unittest.mock import Mock

from aiohttp.abc import Request
from aiounittest import async_test
from asyncmock import AsyncMock

from news_service_lib.uaa_service import UaaService
from webapp.container_config import container
from webapp.middlewares import uaa_auth_middleware


class TestMiddlewares(TestCase):
    """
    Middlewares test cases implementation
    """
    def setUp(self) -> None:
        """
        Set up the tests environment
        """
        container.reset()
        self.uaa_service = AsyncMock(spec=UaaService)
        container.set('uaa_service', self.uaa_service)

    @async_test
    async def test_uaa_auth_middleware_from_header(self):
        """
        Test calling the uaa auth middleware with a request with the token in headers validates the token
        and sets its user field
        """
        test_token = 'test_token'
        request_mock = Mock(spec=Request)
        request_mock.headers = {'X-API-Key': test_token}
        handler_mock = AsyncMock()
        handled_middleware = await uaa_auth_middleware(None, handler_mock)
        await handled_middleware(request_mock)
        self.uaa_service.validate_token.assert_called_with(test_token)
        self.assertIsNotNone(request_mock.user)

    @async_test
    async def test_uaa_auth_middleware_from_cookies(self):
        """
        Test calling the uaa auth middleware with a request with the token in cookies validates the token
        and sets its user field
        """
        test_token = 'test_token'
        request_mock = Mock(spec=Request)
        request_mock.headers = {}
        request_mock.cookies = {'JWT_TOKEN': test_token}
        handler_mock = AsyncMock()
        handled_middleware = await uaa_auth_middleware(None, handler_mock)
        await handled_middleware(request_mock)
        self.uaa_service.validate_token.assert_called_with('Bearer ' + test_token)
        self.assertIsNotNone(request_mock.user)

    @async_test
    async def test_uaa_auth_middleware_no_token(self):
        """
        Test calling the uaa auth middleware with a request without do not call to validate the token
        and its user field is None
        """
        request_mock = Mock(spec=Request)
        request_mock.headers = {}
        request_mock.cookies = {}
        handler_mock = AsyncMock()
        handled_middleware = await uaa_auth_middleware(None, handler_mock)
        await handled_middleware(request_mock)
        self.uaa_service.validate_token.assert_not_called()
        self.assertIsNone(request_mock.user)