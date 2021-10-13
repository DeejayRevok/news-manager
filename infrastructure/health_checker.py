from infrastructure.storage.mongo_storage_client import MongoStorageClient
from news_service_lib.healthcheck import HealthChecker


class NewsManagerHealthChecker(HealthChecker):
    def __init__(self, mongo_storage_client: MongoStorageClient):
        self.__mongo_client = mongo_storage_client

    def health_check(self) -> bool:
        return self.__mongo_client.health_check()
