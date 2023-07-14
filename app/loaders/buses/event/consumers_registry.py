from bus_station.event_terminal.event_consumer_registry import EventConsumerRegistry
from yandil.container import default_container

from application.save_new.new_discovered_event_consumer import NewDiscoveredEventConsumer
from application.save_new.new_hydrated_event_consumer import NewHydratedEventConsumer


def register() -> None:
    registry = default_container[EventConsumerRegistry]

    registry.register(default_container[NewDiscoveredEventConsumer])
    registry.register(default_container[NewHydratedEventConsumer])
