from pypendency.argument import Argument
from pypendency.builder import container_builder
from pypendency.definition import Definition


def load() -> None:
    container_builder.set_definition(
        Definition(
            "application.save_new.save_new_command_handler.SaveNewCommandHandler",
            "application.save_new.save_new_command_handler.SaveNewCommandHandler",
            [
                Argument.no_kw_argument("@infrastructure.mongo.mongo_new_repository.MongoNewRepository"),
                Argument.no_kw_argument(
                    "@bus_station.event_terminal.bus.asynchronous.distributed.kombu_event_bus.KombuEventBus"
                ),
                Argument.no_kw_argument("@logging.Logger"),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "application.save_new.new_discovered_event_consumer.NewDiscoveredEventConsumer",
            "application.save_new.new_discovered_event_consumer.NewDiscoveredEventConsumer",
            [
                Argument.no_kw_argument("@infrastructure.mongo.mongo_new_repository.MongoNewRepository"),
                Argument.no_kw_argument(
                    "@bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus"
                ),
            ],
        )
    )
    container_builder.set_definition(
        Definition(
            "application.save_new.new_hydrated_event_consumer.NewHydratedEventConsumer",
            "application.save_new.new_hydrated_event_consumer.NewHydratedEventConsumer",
            [Argument.no_kw_argument("@bus_station.command_terminal.bus.synchronous.sync_command_bus.SyncCommandBus")],
        )
    )
