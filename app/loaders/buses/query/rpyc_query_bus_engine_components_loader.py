from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "bus_station.passengers.serialization.passenger_json_deserializer.PassengerJSONDeserializer",
            "bus_station.passengers.serialization.passenger_json_deserializer.PassengerJSONDeserializer",
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.query_terminal.serialization.query_response_json_serializer.QueryResponseJSONSerializer",
            "bus_station.query_terminal.serialization.query_response_json_serializer.QueryResponseJSONSerializer",
        )
    )
    container_builder.set_definition(
        Definition(
            "bus_station.query_terminal.registry.redis_query_registry.RedisQueryRegistry",
            "bus_station.query_terminal.registry.redis_query_registry.RedisQueryRegistry",
            [
                Argument(
                    "redis_repository",
                    "@bus_station.passengers.passenger_record"
                    ".redis_passenger_record_repository.RedisPassengerRecordRepository",
                ),
                Argument(
                    "query_handler_resolver",
                    "@bus_station.shared_terminal.bus_stop_resolver"
                    ".pypendency_bus_stop_resolver.PypendencyBusStopResolver",
                ),
                Argument("fqn_getter", "@bus_station.shared_terminal.fqn_getter.FQNGetter"),
                Argument(
                    "passenger_class_resolver",
                    "@bus_station.passengers.passenger_class_resolver.PassengerClassResolver",
                ),
            ],
        )
    )
