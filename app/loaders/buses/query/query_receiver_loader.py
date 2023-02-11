from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "bus_station.query_terminal.middleware.query_middleware_receiver.QueryMiddlewareReceiver",
            "bus_station.query_terminal.middleware.query_middleware_receiver.QueryMiddlewareReceiver",
        )
    )
