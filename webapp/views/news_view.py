from logging import Logger

from aiohttp import web
from news_service_lib.decorators import login_required
from time import strptime, mktime
from aiohttp.web_app import Application
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp.web_request import Request
from aiohttp.web_response import json_response, Response
from aiohttp_apispec import docs

from services.news_service import NewsService
from webapp.definitions import API_VERSION


class NewsView:
    __DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    __ROOT_PATH = "/api/news"

    def __init__(self, web_container: Application, news_service: NewsService, logger: Logger):
        self.__news_service = news_service
        self.__logger = logger
        self.__setup_routes(web_container)

    def __setup_routes(self, web_container: Application) -> None:
        web_container.add_routes(
            [
                web.get(f"/{API_VERSION}{self.__ROOT_PATH}", self.get_news, allow_head=False),
            ]
        )

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
        @login_required
        async def request_executor(inner_request):
            self.__logger.info("REST request to get all news")

            try:
                start_date = (
                    mktime(strptime(inner_request.rel_url.query["start_date"], self.__DATE_FORMAT))
                    if "start_date" in inner_request.rel_url.query
                    else None
                )
                end_date = (
                    mktime(strptime(inner_request.rel_url.query["end_date"], self.__DATE_FORMAT))
                    if "end_date" in inner_request.rel_url.query
                    else None
                )
            except Exception as ex:
                raise HTTPBadRequest(text=str(ex))

            news = list(
                map(
                    lambda new: new.dto(self.__DATE_FORMAT),
                    await self.__news_service.get_news_filtered(from_date=start_date, to_date=end_date),
                )
            )

            return json_response(news, status=200)

        return await request_executor(request)
