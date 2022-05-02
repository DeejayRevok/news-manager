import pymongo
from pymongo.errors import ServerSelectionTimeoutError

from typing import List, Iterator

from infrastructure.storage.filter.filter import Filter
from infrastructure.storage.filter.mongo_filter_parser import MongoFilterParser
from infrastructure.storage.mongo_sort_direction import MongoSortDirection


class MongoStorageClient:
    def __init__(self, members: str, rsname: str, database: str):
        self.__mongo_client = pymongo.MongoClient(members, replicaset=rsname, connect=True)
        self.__database = self.__mongo_client[database]
        self.__collection = None

    def __check_collection(self) -> None:
        if self.__collection is None:
            raise AttributeError("Collection not set")

    def health_check(self) -> bool:
        try:
            self.__mongo_client.server_info()
            return True
        except ServerSelectionTimeoutError:
            return False

    def save(self, item: dict):
        self.__check_collection()
        self.__collection.insert_one(item)

    @staticmethod
    def __parse_filters(filters: List[Filter]) -> dict:
        aggregated_query = {}
        if filters is not None and len(filters) > 0:
            for filter_instance in filters:
                query = filter_instance.parse_filter(MongoFilterParser)
                aggregated_query = {**aggregated_query, **query}
        return aggregated_query

    def get(
        self, filters: List[Filter] = None, sort_key: str = None, sort_direction: MongoSortDirection = None
    ) -> Iterator[dict]:
        self.__check_collection()
        cursor = self.__collection.find(self.__parse_filters(filters))

        if sort_key:
            cursor = cursor.sort(sort_key, sort_direction.value)

        for item in cursor:
            yield item

    def get_one(self, filters: List[Filter] = None) -> dict:
        self.__check_collection()
        return self.__collection.find_one(self.__parse_filters(filters))

    def delete(self, identifier: str):
        self.__check_collection()
        self.__collection.remove(identifier)

    def consume_inserts(self) -> Iterator[dict]:
        self.__check_collection()
        insert_consumer = self.__collection.watch([{"$match": {"operationType": "insert"}}])
        try:
            for insert_change in insert_consumer:
                yield insert_change["fullDocument"]
        except Exception as ex:
            insert_consumer.close()
            raise ex
        except KeyboardInterrupt as kex:
            insert_consumer.close()
            raise kex

    def set_collection(self, collection: str):
        self.__collection = self.__database[collection]
