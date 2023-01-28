from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class NewsManagerHealthChecker:
    def __init__(self, mongo_client: MongoClient):
        self.__mongo_client = mongo_client

    def health_check(self) -> bool:
        return self.__mongo_health_check()

    def __mongo_health_check(self) -> bool:
        try:
            self.__mongo_client.server_info()
            return True
        except ServerSelectionTimeoutError:
            return False
