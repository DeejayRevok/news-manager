from os import environ

from bus_station.bus_stop.registration.address.redis_bus_stop_address_registry import RedisBusStopAddressRegistry
from bus_station.query_terminal.query_handler_registry import QueryHandlerRegistry
from yandil.container import default_container

from application.get_new.get_new_query_handler import GetNewQueryHandler
from application.get_news.get_news_query_handler import GetNewsQueryHandler


def register() -> None:
    registry = default_container[QueryHandlerRegistry]
    registry.register(default_container[GetNewsQueryHandler])
    registry.register(default_container[GetNewQueryHandler])

    address_registry = default_container[RedisBusStopAddressRegistry]

    get_new_host = environ.get("NEWS_MANAGER_RPYC_GET_NEW_HOST")
    get_new_port = int(environ.get("NEWS_MANAGER_RPYC_GET_NEW_PORT"))
    address_registry.register(GetNewQueryHandler, f"{get_new_host}:{get_new_port}")
