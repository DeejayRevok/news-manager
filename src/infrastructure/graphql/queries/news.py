from dataclasses import asdict
from datetime import datetime
from typing import List

from graphene import ObjectType, List as GraphList, Field, Argument, String, Boolean, Float
from pypendency.builder import container_builder

from application.get_new.get_new_query import GetNewQuery
from application.get_news.get_news_query import GetNewsQuery
from infrastructure.graphql.custom_date_time import CustomDateTime
from infrastructure.graphql.models.new import New


class NewsQuery(ObjectType):
    news = GraphList(
        New,
        source=Argument(String, required=False),
        hydration=Argument(Boolean, required=False),
        from_sentiment=Argument(Float, required=False),
        to_sentiment=Argument(Float, required=False),
        from_date=Argument(CustomDateTime, name="fromDate", required=False),
        to_date=Argument(CustomDateTime, name="toDate", required=False),
        description="News filtered with the given filters",
    )
    new = Field(New, title=Argument(String, required=True), description="New with the given title")

    async def resolve_news(
        self,
        _,
        source: str = None,
        hydration: bool = None,
        from_sentiment: float = None,
        to_sentiment: float = None,
        from_date: datetime = None,
        to_date: datetime = None,
    ) -> List[dict]:
        query_bus = container_builder.get("bus_station.query_terminal.bus.synchronous.sync_query_bus.SyncQueryBus")
        query = GetNewsQuery(
            source=source,
            hydrated=hydration,
            from_date=from_date.isoformat() if from_date is not None else None,
            to_date=to_date.isoformat() if to_date is not None else None,
            from_sentiment=from_sentiment,
            to_sentiment=to_sentiment
        )
        query_result = query_bus.transport(query)

        return [asdict(new) for new in query_result.data]

    async def resolve_new(self, _, title: str) -> dict:
        query_bus = container_builder.get("bus_station.query_terminal.bus.synchronous.sync_query_bus.SyncQueryBus")
        query = GetNewQuery(
            title=title
        )
        query_result = query_bus.transport(query)
        return asdict(query_result.data)
