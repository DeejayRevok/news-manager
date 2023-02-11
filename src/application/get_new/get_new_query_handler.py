from logging import Logger

from bus_station.query_terminal.query_handler import QueryHandler
from bus_station.query_terminal.query_response import QueryResponse

from application.get_new.get_new_query import GetNewQuery
from domain.new.new_not_found_exception import NewNotFoundException
from domain.new.new_repository import NewRepository


class GetNewQueryHandler(QueryHandler):
    def __init__(self, new_repository: NewRepository, logger: Logger):
        self.__new_repository = new_repository
        self.__logger = logger

    def handle(self, query: GetNewQuery) -> QueryResponse:
        self.__logger.info(f"Start getting new with title {query.title}")

        new = self.__new_repository.find_by_title(query.title)
        if new is None:
            raise NewNotFoundException(query.title)

        self.__logger.info(f"Finish getting new with title {query.title}")
        return QueryResponse(data=new)

    @classmethod
    def bus_stop_name(cls) -> str:
        return "query_handler.news_manager.get_new"
