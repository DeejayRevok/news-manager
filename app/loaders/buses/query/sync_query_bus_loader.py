from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "bus_station.query_terminal.registry.in_memory_query_registry.InMemoryQueryRegistry",
            "bus_station.query_terminal.registry.in_memory_query_registry.InMemoryQueryRegistry",
            [
                Argument("in_memory_repository", "@bus_station.passengers.passenger_record.in_memory_passenger_record_repository.InMemoryPassengerRecordRepository"),
                Argument("query_handler_resolver", "@bus_station.shared_terminal.bus_stop_resolver.pypendency_bus_stop_resolver.PypendencyBusStopResolver"),
                Argument("fqn_getter", "@bus_station.shared_terminal.fqn_getter.FQNGetter"),
                Argument("passenger_class_resolver", "@bus_station.passengers.passenger_class_resolver.PassengerClassResolver")
            ]
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.query_terminal.bus.synchronous.sync_query_bus.SyncQueryBus",
            "bus_station.query_terminal.bus.synchronous.sync_query_bus.SyncQueryBus",
            [
                Argument.no_kw_argument("@bus_station.query_terminal.registry.in_memory_query_registry.InMemoryQueryRegistry"),
                Argument.no_kw_argument("@bus_station.query_terminal.middleware.query_middleware_receiver.QueryMiddlewareReceiver")
            ]
        )
    )
