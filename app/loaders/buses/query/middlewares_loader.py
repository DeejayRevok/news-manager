from bus_station.query_terminal.middleware.implementations.logging_query_middleware import LoggingQueryMiddleware
from bus_station.query_terminal.middleware.implementations.timing_query_middleware import TimingQueryMiddleware
from bus_station.query_terminal.middleware.query_middleware_receiver import QueryMiddlewareReceiver
from pypendency.builder import container_builder

from infrastructure.apm.apm_query_middleware import APMQueryMiddleware


def load() -> None:
    query_middleware_receiver: QueryMiddlewareReceiver = container_builder.get(
        "bus_station.query_terminal.middleware.query_middleware_receiver.QueryMiddlewareReceiver"
    )
    query_middleware_receiver.add_middleware_definition(
        LoggingQueryMiddleware, container_builder.get("logging.Logger"), lazy=False
    )
    query_middleware_receiver.add_middleware_definition(
        TimingQueryMiddleware, container_builder.get("logging.Logger"), lazy=True
    )
    query_middleware_receiver.add_middleware_definition(
        APMQueryMiddleware, container_builder.get("elasticapm.Client"), lazy=False
    )
