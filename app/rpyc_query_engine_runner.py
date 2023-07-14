from argparse import ArgumentParser

from bus_station.bus_stop.bus_stop import BusStop
from bus_station.bus_stop.registration.address.redis_bus_stop_address_registry import RedisBusStopAddressRegistry
from bus_station.passengers.serialization.passenger_json_deserializer import PassengerJSONDeserializer
from bus_station.query_terminal.bus_engine.rpyc_query_bus_engine import RPyCQueryBusEngine
from bus_station.query_terminal.middleware.query_middleware_receiver import QueryMiddlewareReceiver
from bus_station.query_terminal.query_handler_registry import QueryHandlerRegistry
from bus_station.query_terminal.rpyc_query_server import RPyCQueryServer
from bus_station.query_terminal.serialization.query_response_json_serializer import QueryResponseJSONSerializer
from bus_station.shared_terminal.engine.runner.self_process_engine_runner import SelfProcessEngineRunner
from yandil.container import default_container

from app.loaders import load_app


def run() -> None:
    load_app()
    args = __load_args()
    query_registry = default_container[QueryHandlerRegistry]
    query_handler_name = args["query_handler_name"]
    query_handler_class = __get_bus_stop_from_name(query_handler_name)
    port = __get_port(query_handler_class)
    rpyc_server = RPyCQueryServer(
        host=args["host"],
        port=port,
        query_deserializer=default_container[PassengerJSONDeserializer],
        query_receiver=default_container[QueryMiddlewareReceiver],
        query_response_serializer=default_container[QueryResponseJSONSerializer],
    )
    engine = RPyCQueryBusEngine(rpyc_server, query_registry, query_handler_name)
    SelfProcessEngineRunner(engine).run()


def __load_args() -> dict:
    arg_solver = ArgumentParser(description="RPyC query engine runner")
    arg_solver.add_argument("-ht", "--host", required=True, help="Query engine running host address")
    arg_solver.add_argument("-qhn", "--query_handler_name", required=True, help="Query handler name")

    return vars(arg_solver.parse_args())


def __get_port(query_handler: BusStop) -> int:
    address = default_container[RedisBusStopAddressRegistry].get_address_for_bus_stop_passenger_class(
        query_handler.passenger()
    )
    return address.split(":")[1]


def __get_bus_stop_from_name(name: str) -> BusStop:
    return default_container[QueryHandlerRegistry].get_bus_stop_by_name(name)


if __name__ == "__main__":
    run()
