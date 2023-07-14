import os

from redis import Redis
from yandil.container import default_container


def load() -> None:
    redis_host = os.environ.get("NEWS_MANAGER_REDIS__HOST")
    redis_port = int(os.environ.get("NEWS_MANAGER_REDIS__PORT"))
    redis_password = os.environ.get("NEWS_MANAGER_REDIS__PASSWORD")
    redis_client = Redis(host=redis_host, port=redis_port, password=redis_password)
    default_container[Redis] = redis_client
