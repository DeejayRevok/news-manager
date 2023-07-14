import os

from pymongo import MongoClient
from pymongo.database import Database
from yandil.container import default_container


def load() -> None:
    mongo_host = os.environ.get("NEWS_MANAGER_MONGO__HOST")
    mongo_port = int(os.environ.get("NEWS_MANAGER_MONGO__PORT"))
    mongo_database = os.environ.get("NEWS_MANAGER_MONGO__DATABASE")
    mongo_client = MongoClient(
        host=mongo_host,
        port=mongo_port,
    )
    mongo_db = mongo_client[mongo_database]
    default_container[MongoClient] = mongo_client
    default_container[Database] = mongo_db
