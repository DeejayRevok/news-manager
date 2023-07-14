from bus_station.query_terminal.bus.synchronous.sync_query_bus import SyncQueryBus
from bus_station.query_terminal.middleware.query_middleware_receiver import QueryMiddlewareReceiver
from bus_station.query_terminal.query_handler_registry import QueryHandlerRegistry
from yandil.container import default_container


def load() -> None:
    default_container.add(QueryMiddlewareReceiver)
    default_container.add(QueryHandlerRegistry)
    default_container.add(SyncQueryBus, is_primary=True)
