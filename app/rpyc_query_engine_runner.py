from argparse import ArgumentParser

from bus_station.query_terminal.bus_engine.rpyc_query_bus_engine import RPyCQueryBusEngine
from bus_station.query_terminal.registry.redis_query_registry import RedisQueryRegistry
from bus_station.query_terminal.rpyc_query_server import RPyCQueryServer
from bus_station.shared_terminal.engine.runner.self_process_engine_runner import SelfProcessEngineRunner
from pypendency.builder import container_builder

from app.loaders import load_app


def run() -> None:
    load_app()
    args = __load_args()
    query_registry = container_builder.get(
        "bus_station.query_terminal.registry.redis_query_registry.RedisQueryRegistry"
    )
    query_name = args["query"]
    query_port = __get_query_registered_port(query_name, query_registry)
    rpyc_server = RPyCQueryServer(
        host=args["host"],
        port=query_port,
        query_deserializer=container_builder.get(
            "bus_station.passengers.serialization.passenger_json_deserializer.PassengerJSONDeserializer"
        ),
        query_receiver=container_builder.get(
            "bus_station.query_terminal.middleware.query_middleware_receiver.QueryMiddlewareReceiver"
        ),
        query_response_serializer=container_builder.get(
            "bus_station.query_terminal.serialization.query_response_json_serializer.QueryResponseJSONSerializer"
        ),
    )
    engine = RPyCQueryBusEngine(rpyc_server, query_registry, query_name)
    SelfProcessEngineRunner(engine).run()


def __load_args() -> dict:
    arg_solver = ArgumentParser(description="RPyC query engine runner")
    arg_solver.add_argument("-ht", "--host", required=True, help="Query engine running host address")
    arg_solver.add_argument("-q", "--query", required=True, help="Query name")

    return vars(arg_solver.parse_args())


def __get_query_registered_port(query_name: str, query_registry: RedisQueryRegistry) -> int:
    query_contact_str = query_registry.get_query_destination_contact(query_name)
    return int(query_contact_str.split(":")[1])


if __name__ == "__main__":
    run()
