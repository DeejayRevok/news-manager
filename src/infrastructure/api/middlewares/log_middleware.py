from logging import Logger
from typing import Callable

from aiohttp.web_request import Request
from aiohttp.web_response import Response


class LogMiddleware:
    def __init__(self, logger: Logger):
        self.__logger = logger

    async def middleware(self, _, handler: Callable):
        async def middleware_handler(request: Request) -> Response:
            response: Response = await handler(request)
            self.__logger.info(f"Executed HTTP request to {request.url} with response status {response.status}")
            return response
        return middleware_handler
