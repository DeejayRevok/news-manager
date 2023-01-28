from dataclasses import asdict
from typing import Optional, Iterable

from dacite import from_dict
from pymongo.database import Database

from domain.new.find_news_criteria import FindNewsCriteria
from domain.new.new import New
from domain.new.new_repository import NewRepository


class MongoNewRepository(NewRepository):
    __COLLECTION_NAME = "new"

    def __init__(self, mongo_db: Database):
        self.__collection = mongo_db[self.__COLLECTION_NAME]

    def save(self, new: New) -> None:
        self.__collection.replace_one(
            filter={"title": new.title},
            replacement=asdict(new),
            upsert=True
        )

    def find_by_title(self, title: str) -> Optional[New]:
        result = self.__collection.find_one({"title": title})
        if result is None:
            return None
        return from_dict(New, result)

    def find_by_criteria(self, criteria: FindNewsCriteria) -> Iterable[New]:
        filters = {}
        if criteria.source is not None:
            filters["source"] = criteria.source

        if criteria.hydrated is not None:
            filters["hydrated"] = criteria.hydrated

        if criteria.from_date is not None:
            filters.update({"date": {"$gt": criteria.from_date}})

        if criteria.to_date is not None:
            filters.update({"date": {"$lt": criteria.to_date}})

        if criteria.from_sentiment is not None:
            filters.update({"sentiment": {"$gt": criteria.from_sentiment}})

        if criteria.to_sentiment is not None:
            filters.update({"sentiment": {"$lt": criteria.to_sentiment}})

        for result in self.__collection.find(filters):
            yield from_dict(New, result)
