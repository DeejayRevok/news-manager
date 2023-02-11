from bus_station.event_terminal.registry.event_registry import EventRegistry
from pypendency.builder import container_builder

from domain.new.new_discovered_event import NewDiscoveredEvent
from domain.new.new_hydrated_event import NewHydratedEvent


def register() -> None:
    registry: EventRegistry = container_builder.get(
        "bus_station.event_terminal.registry.redis_event_registry.RedisEventRegistry"
    )
    new_discovered_consumer = container_builder.get(
        "application.save_new.new_discovered_event_consumer.NewDiscoveredEventConsumer"
    )
    registry.register(new_discovered_consumer, NewDiscoveredEvent.passenger_name())
    new_processed_consumer = container_builder.get(
        "application.save_new.new_hydrated_event_consumer.NewHydratedEventConsumer"
    )
    registry.register(new_processed_consumer, NewHydratedEvent.passenger_name())
