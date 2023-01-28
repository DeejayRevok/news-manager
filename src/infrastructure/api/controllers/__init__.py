from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "infrastructure.api.controllers.get_news_controller.GetNewsController",
            "infrastructure.api.controllers.get_news_controller.GetNewsController",
            [
                Argument.no_kw_argument("@bus_station.query_terminal.bus.synchronous.sync_query_bus.SyncQueryBus"),
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
