from dataclasses import asdict

from infrastructure.storage.filter.match_filter import MatchFilter
from infrastructure.storage.filter.range_filter import RangeFilter
from infrastructure.storage.mongo_sort_direction import MongoSortDirection
from news_service_lib.models.new import New
from typing import Iterator, Tuple

from dacite import from_dict

from infrastructure.storage.mongo_storage_client import MongoStorageClient


class NewsService:
    def __init__(self, client: MongoStorageClient):
        self.__client = client
        self.__client.set_collection("new")

    async def save_new(self, new: New):
        await self.delete_new(new)
        self.__client.save(asdict(new))

    async def get_new_by_title(self, title: str) -> New:
        found_new = self.__client.get_one(filters=[MatchFilter("title", title)])

        if found_new is not None:
            return self.__render_new(found_new)
        else:
            raise KeyError(f"New with title {title} not found")

    async def get_news_filtered(
        self,
        source: str = None,
        hydration: bool = None,
        sentiment: Tuple[float, bool] = None,
        from_date: float = None,
        to_date: float = None,
    ) -> Iterator[New]:
        filters_list = list()

        if source is not None:
            filters_list.append(MatchFilter("source", source))

        if hydration is not None:
            filters_list.append(MatchFilter("hydrated", hydration))

        if sentiment is not None and sentiment[0] is not None:
            if sentiment[1]:
                filters_list.append(RangeFilter("sentiment", lower=sentiment[0]))
            else:
                filters_list.append(RangeFilter("sentiment", upper=sentiment[0]))

        if from_date is not None or to_date is not None:
            filters_list.append(RangeFilter("date", lower=from_date, upper=to_date))

        return self.__render_news_list(
            self.__client.get(filters_list, sort_key="date", sort_direction=MongoSortDirection.DESC)
        )

    async def delete_new(self, new: New):
        new_delete = self.__client.get_one(filters=[MatchFilter("title", new.title)])
        if new_delete:
            self.__client.delete(new_delete["_id"])

    def consume_new_inserts(self) -> Iterator[Tuple[str, New]]:
        for document in self.__client.consume_inserts():
            yield str(document["_id"]), self.__render_new(document)

    def __render_news_list(self, news_list: Iterator[dict]) -> Iterator[New]:
        for new in news_list:
            yield self.__render_new(new)

    def __render_new(self, new: dict) -> New:
        if "_id" in new:
            del new["_id"]
        return from_dict(New, new)
