from http import HTTPStatus
from typing import Callable

from aiohttp.abc import Application, Request
from aiohttp.web_exceptions import HTTPException
from aiohttp.web_response import Response
from elasticapm import Client


class APMMiddleware:
    def __init__(self, apm_client: Client):
        self.__apm_client = apm_client

    async def middleware(self, _: Application, request_handler: Callable) -> Callable:
        async def middleware_handler(request: Request) -> Response:
            try:
                self.__apm_client.begin_transaction("request")
                response = await request_handler(request)
                self.__apm_client.end_transaction(f"{request.method}{request.rel_url}", response.status)
                return response
            except HTTPException as httpeex:
                self.__apm_client.end_transaction(f"{request.method}{request.rel_url}", httpeex.status)
                self.__apm_client.capture_exception()
                raise httpeex
            except Exception as ex:
                self.__apm_client.end_transaction(
                    f"{request.method}{request.rel_url}", HTTPStatus.INTERNAL_SERVER_ERROR
                )
                self.__apm_client.capture_exception()
                raise ex

        return middleware_handler
