from dataclasses import asdict
from datetime import datetime
from logging import Logger

from aiohttp.web_exceptions import HTTPBadRequest, HTTPInternalServerError
from aiohttp.web_request import Request
from aiohttp.web_response import json_response, Response
from aiohttp_apispec import docs
from bus_station.query_terminal.bus.query_bus import QueryBus

from application.get_news.get_news_query import GetNewsQuery


class GetNewsController:

    def __init__(self, query_bus: QueryBus, logger: Logger):
        self.__query_bus = query_bus
        self.__logger = logger

    @docs(
        tags=["News"],
        summary="News list",
        description="Get available news",
        parameters=[
            {
                "in": "query",
                "name": "start_date",
                "type": "string",
                "format": "date-time",
                "description": "Start date to filter news",
                "required": False,
            },
            {
                "in": "query",
                "name": "end_date",
                "type": "string",
                "format": "date-time",
                "description": "End date to filter news",
                "required": False,
            },
        ],
        security=[{"ApiKeyAuth": []}],
    )
    async def get_news(self, request: Request) -> Response:
        async def request_executor(inner_request):
            self.__logger.info("REST request to get all news")

            try:
                start_date = (
                    datetime.fromisoformat(inner_request.rel_url.query["start_date"])
                    if "start_date" in inner_request.rel_url.query
                    else None
                )
                end_date = (
                    datetime.fromisoformat(inner_request.rel_url.query["end_date"])
                    if "end_date" in inner_request.rel_url.query
                    else None
                )
            except Exception as ex:
                raise HTTPBadRequest(text=str(ex))

            query = GetNewsQuery(
                from_date=start_date,
                to_date=end_date
            )
            try:
                query_result = self.__query_bus.transport(query)
            except Exception as ex:
                raise HTTPInternalServerError(text=str(ex))

            news = [asdict(new) for new in query_result.data]

            return json_response(news, status=200)

        return await request_executor(request)
