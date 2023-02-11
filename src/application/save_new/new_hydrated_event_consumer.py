from bus_station.command_terminal.bus.command_bus import CommandBus
from bus_station.event_terminal.event_consumer import EventConsumer

from application.save_new.save_new_command import SaveNewCommand
from domain.new.new_hydrated_event import NewHydratedEvent


class NewHydratedEventConsumer(EventConsumer):
    def __init__(self, command_bus: CommandBus):
        self.__command_bus = command_bus

    def consume(self, event: NewHydratedEvent) -> None:
        self.__command_bus.transport(self.__create_command_from_event(event))

    def __create_command_from_event(self, event: NewHydratedEvent) -> SaveNewCommand:
        return SaveNewCommand(
            title=event.title,
            url=event.url,
            content=event.content,
            source=event.source,
            date=event.date,
            language=event.language,
            hydrated=event.hydrated,
            entities=event.entities,
            summary=event.summary,
            sentiment=event.sentiment,
            image=event.image,
        )

    @classmethod
    def bus_stop_name(cls) -> str:
        return "event_consumer.news_manager.save_new.new_hydrated"
