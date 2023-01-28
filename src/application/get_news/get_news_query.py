from dataclasses import dataclass
from typing import Optional

from bus_station.query_terminal.query import Query


@dataclass(frozen=True)
class GetNewsQuery(Query):
    source: Optional[str] = None
    hydrated: Optional[bool] = None
    from_sentiment: Optional[float] = None
    to_sentiment: Optional[float] = None
    from_date: Optional[str] = None
    to_date: Optional[str] = None

    @classmethod
    def passenger_name(cls) -> str:
        return "query.news_manager.get_news"