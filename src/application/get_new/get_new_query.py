from dataclasses import dataclass

from bus_station.query_terminal.query import Query


@dataclass(frozen=True)
class GetNewQuery(Query):
    title: str

    @classmethod
    def passenger_name(cls) -> str:
        return "query.news_manager.get_new"
