"""
News service module
"""
from dataclasses import asdict
from typing import Iterator, Tuple, Union

from dacite import from_dict

from news_service_lib.models import New
from news_service_lib.storage.implementation import MongoStorage
from news_service_lib.storage.filter import MatchFilter
from news_service_lib.storage.filter import RangeFilter
from news_service_lib.storage import SortDirection
from news_service_lib.storage.implementation import Storage
from news_service_lib.storage import StorageWatcher


class NewsService:
    """
    Class used to manage the interaction with the news
    """

    def __init__(self, client: Union[Storage, StorageWatcher]):
        """
        Initialize the NEWS service with the specified storage client

        Args:
            client: storage client
        """
        self._client = client
        self._watcher = client
        if isinstance(self._client, MongoStorage):
            self._client.set_collection('new')

    async def save_new(self, new: New):
        """
        Persist the specified new

        Args:
            new: new to persist

        """
        await self.delete_new(new)
        self._client.save(asdict(new))

    async def get_new_by_title(self, title: str) -> New:
        """
        Get an stored new looking for it by title

        Args:
            title: title of the new to search for

        Returns: found new with the specified title

        """
        found_new = self._client.get_one(filters=[MatchFilter('title', title)])

        if found_new is not None:
            return NewsService._render_new(found_new)
        else:
            raise KeyError(f'New with title {title} not found')

    async def get_news_filtered(self, source: str = None, hydration: bool = None,
                                sentiment: Tuple[float, bool] = None, from_date: float = None,
                                to_date: float = None) -> Iterator[New]:
        """
        Filter news

        Args:
            source: news source filter
            hydration: news hydration flag filter
            sentiment: news sentiment threshold filter
            from_date: news start date to filter
            to_date: news end date to filter

        Returns: filtered news
        """
        filters_list = list()

        if source is not None:
            filters_list.append(MatchFilter('source', source))

        if hydration is not None:
            filters_list.append(MatchFilter('hydrated', hydration))

        if sentiment is not None and sentiment[0] is not None:
            if sentiment[1]:
                filters_list.append(RangeFilter('sentiment', lower=sentiment[0]))
            else:
                filters_list.append(RangeFilter('sentiment', upper=sentiment[0]))

        if from_date is not None or to_date is not None:
            filters_list.append(RangeFilter('date', lower=from_date, upper=to_date))

        return NewsService._render_news_list(
            self._client.get(filters_list, sort_key="date", sort_direction=SortDirection.DESC))

    async def delete_new(self, new: New):
        """
        Delete the input new

        Args:
            new: new to delete

        """
        new_delete = self._client.get_one(filters=[MatchFilter('title', new.title)])
        if new_delete:
            self._client.delete(new_delete['_id'])

    def consume_new_inserts(self) -> Iterator[Tuple[str, New]]:
        """
        Consume the new insertions

        Returns: an iterator to the inserted news

        """
        for document in self._client.consume_inserts():
            yield str(document['_id']), self._render_new(document)

    @staticmethod
    def _render_news_list(news_list: Iterator[dict]) -> Iterator[New]:
        """
        Render the news from the specified list

        Args:
            news_list: news to render

        Returns: iterator to the rendered news

        """
        for new in news_list:
            yield NewsService._render_new(new)

    @staticmethod
    def _render_new(new: dict) -> New:
        """
        Render a single new

        Args:
            new: new to render

        Returns: rendered new

        """
        if '_id' in new:
            del new['_id']
        return from_dict(New, new)
