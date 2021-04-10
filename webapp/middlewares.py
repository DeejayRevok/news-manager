"""
News manager middlewares module
"""
from typing import Callable

from aiohttp.web_exceptions import HTTPException
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from news_service_lib.error_utils import json_error

from log_config import get_logger
from webapp.container_config import container

LOGGER = get_logger()


async def error_middleware(_, handler: Callable):
    """
    This middleware handles exceptions received from views or previous middleware.

    Args:
        handler: request handler

    Returns: error middleware

    """

    async def middleware(request: Request) -> Response:
        apm = container.get('apm')
        try:
            apm.begin_transaction('request')
            response = await handler(request)
            apm.end_transaction(f'{request.method}{request.rel_url}', response.status)
            return response
        except HTTPException as ex:
            LOGGER.error('Request %s has failed with exception: %s', request, repr(ex))
            apm.end_transaction(f'{request.method}{request.rel_url}', ex.status)
            apm.capture_exception()
            return json_error(ex.status, ex)
        except Exception as ex:
            LOGGER.error('Request %s has failed with exception: %s', request, repr(ex), exc_info=True)
            apm.end_transaction(f'{request.method}{request.rel_url}', 500)
            apm.capture_exception()
            return json_error(500, ex)

    return middleware


async def uaa_auth_middleware(_, handler: Callable):
    """
    This middlewares check if the requests are authenticated using the uaa service

    Args:
        handler: request handler

    Returns: authentication middleware

    """

    async def middleware(request: Request) -> Response:
        request.user = None
        jwt_token = request.headers.get('X-API-Key', None)
        if not jwt_token:
            jwt_token = request.cookies.get('JWT_TOKEN', None)
            if jwt_token:
                jwt_token = 'Bearer ' + jwt_token
        if jwt_token:
            request.user = await container.get('uaa_service').validate_token(
                jwt_token)
        return await handler(request)

    return middleware
