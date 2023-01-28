from datetime import datetime
from logging import Logger
from typing import Optional

from bus_station.query_terminal.query_handler import QueryHandler
from bus_station.query_terminal.query_response import QueryResponse

from application.get_news.get_news_query import GetNewsQuery
from domain.new.find_news_criteria import FindNewsCriteria
from domain.new.new_repository import NewRepository


class GetNewsQueryHandler(QueryHandler):
    def __init__(self, new_repository: NewRepository, logger: Logger):
        self.__new_repository = new_repository
        self.__logger = logger

    def handle(self, query: GetNewsQuery) -> QueryResponse:
        self.__logger.info("Starting getting news")

        result_news = list(self.__new_repository.find_by_criteria(self.__create_criteria_from_query(query)))

        self.__logger.info("Finished getting news")
        return QueryResponse(data=result_news)

    def __create_criteria_from_query(self, query: GetNewsQuery) -> FindNewsCriteria:
        return FindNewsCriteria(
            source=query.source,
            hydrated=query.hydrated,
            from_sentiment=query.from_sentiment,
            to_sentiment=query.to_sentiment,
            from_date=self.__get_timestamp_from_date_str(query.from_date),
            to_date=self.__get_timestamp_from_date_str(query.to_date),
        )

    def __get_timestamp_from_date_str(self, date_str: Optional[str]) -> Optional[float]:
        if date_str is None:
            return None
        return datetime.fromisoformat(date_str).timestamp()

    @classmethod
    def bus_stop_name(cls) -> str:
        return "query_handler.news_manager.get_news"
