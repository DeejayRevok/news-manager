import os

from bus_station.query_terminal.registry.redis_query_registry import RedisQueryRegistry
from pypendency.builder import container_builder


def register() -> None:
    in_memory_registry = container_builder.get(
        "bus_station.query_terminal.registry.in_memory_query_registry.InMemoryQueryRegistry"
    )
    get_news_query_handler = container_builder.get(
        "application.get_news.get_news_query_handler.GetNewsQueryHandler"
    )
    get_new_query_handler = container_builder.get(
        "application.get_new.get_new_query_handler.GetNewQueryHandler"
    )
    in_memory_registry.register(get_news_query_handler, get_news_query_handler)
    in_memory_registry.register(get_new_query_handler, get_new_query_handler)

    redis_registry = container_builder.get(
        "bus_station.query_terminal.registry.redis_query_registry.RedisQueryRegistry",
    )
    
    __register_rpyc_query_handler(
        registry=redis_registry,
        query_handler_fqn="application.get_new.get_new_query_handler.GetNewQueryHandler",
        query_handler_host=os.environ.get("NEWS_MANAGER_RPYC_GET_NEW_HOST"),
        query_handler_port=int(os.environ.get("NEWS_MANAGER_RPYC_GET_NEW_PORT"))
    )


def __register_rpyc_query_handler(registry: RedisQueryRegistry, query_handler_fqn: str, query_handler_host: str, query_handler_port: int) -> None:
    handler = container_builder.get(
            query_handler_fqn
        )
    registry.register(handler, f"{query_handler_host}:{query_handler_port}")
