"""
Graphql news queries module
"""
from dataclasses import asdict
from datetime import datetime
from typing import List

from graphene import ObjectType, List as GraphList, Field, Argument, String, Boolean, Float
from news_service_lib.graphql import login_required, CustomDateTime
from news_service_lib.graphql.model import New

from log_config import get_logger
from services.news_service import NewsService
from webapp.container_config import container

LOGGER = get_logger()


class NewsQuery(ObjectType):
    """
    GraphQL news queries implementation
    """
    news = GraphList(New,
                     source=Argument(String, required=False),
                     hydration=Argument(Boolean, required=False),
                     sentiment=Argument(Float, required=False),
                     higher=Argument(Boolean, required=False),
                     from_date=Argument(CustomDateTime, name='fromDate', required=False),
                     to_date=Argument(CustomDateTime, name='toDate', required=False),
                     description='News filtered with the given filters')
    new = Field(New,
                title=Argument(String, required=True),
                description='New with the given title')

    @login_required
    async def resolve_news(self, _, source: str = None, hydration: bool = None,
                           sentiment: float = None, higher: bool = True, from_date: datetime = None,
                           to_date: datetime = None) -> List[dict]:
        """
        News list graphql query

        Args:
            source: news source filter
            hydration: news hydration flag filter
            sentiment: news sentiment threshold filter
            higher: True if the sentiment filter searches for higher values, False otherwise
            from_date: news date start filter
            to_date: news date end filter

        Returns: list of queried news

        """
        LOGGER.info('Resolving multiple news')
        news_service: NewsService = container.get('news_service')
        return [new.dto(CustomDateTime.DATE_FORMAT) for new in
                await news_service.get_news_filtered(source=source,
                                                     hydration=hydration,
                                                     sentiment=(sentiment, higher),
                                                     from_date=from_date.timestamp() if from_date else None,
                                                     to_date=to_date.timestamp() if to_date else None)]

    @login_required
    async def resolve_new(self, _, title: str) -> dict:
        """
        Single new graphql query

        Args:
            title: title to get new

        Returns: queried new

        """
        LOGGER.info('Resolving new %s', title)
        news_service: NewsService = container.get('news_service')
        return asdict(await news_service.get_new_by_title(title))
