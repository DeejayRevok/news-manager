import os

from pymongo import MongoClient
from pypendency.builder import container_builder


def load() -> None:
    mongo_host = os.environ.get("NEWS_MANAGER_MONGO__HOST")
    mongo_port = int(os.environ.get("NEWS_MANAGER_MONGO__PORT"))
    mongo_database = os.environ.get("NEWS_MANAGER_MONGO__DATABASE")
    mongo_client = MongoClient(
        host=mongo_host,
        port=mongo_port,
    )
    mongo_db = mongo_client[mongo_database]
    container_builder.set("pymongo.MongoClient", mongo_client)
    container_builder.set("pymongo.database.Database", mongo_db)
