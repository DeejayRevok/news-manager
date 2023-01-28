import os

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
    rpyc_query_bus_exposed_host_address = os.environ.get("NEWS_MANAGER_RPYC_QUERY_BUS_EXPOSED_HOST_ADDRESS")
    rpyc_query_bus_port = int(os.environ.get("NEWS_MANAGER_RPYC_QUERY_BUS_STARTING_PORT"))
    rpyc_handlers_fqns = [
        "application.get_new.get_new_query_handler.GetNewQueryHandler"
    ]
    for rpyc_handler_fqn in rpyc_handlers_fqns:
        handler = container_builder.get(
            rpyc_handler_fqn
        )
        redis_registry.register(handler, f"{rpyc_query_bus_exposed_host_address}:{rpyc_query_bus_port}")
        rpyc_query_bus_port += 1
