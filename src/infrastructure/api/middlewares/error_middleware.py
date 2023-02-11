from http import HTTPStatus
from logging import Logger
from typing import Callable

from aiohttp.web_exceptions import HTTPException
from aiohttp.web_request import Request
from aiohttp.web_response import json_response, Response


class ErrorMiddleware:
    def __init__(self, logger: Logger):
        self.__logger = logger

    async def middleware(self, _, handler: Callable):
        async def middleware_handler(request: Request) -> Response:
            try:
                response = await handler(request)
                return response
            except HTTPException as ex:
                self.__logger.exception(ex)
                return json_response(data=dict(error=ex.__class__.__name__, detail=str(ex)), status=ex.status)
            except Exception as ex:
                self.__logger.exception(ex)
                return json_response(
                    data=dict(error=ex.__class__.__name__, detail=str(ex)), status=HTTPStatus.INTERNAL_SERVER_ERROR
                )

        return middleware_handler
