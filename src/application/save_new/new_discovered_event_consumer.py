from bus_station.command_terminal.bus.command_bus import CommandBus
from bus_station.event_terminal.event_consumer import EventConsumer

from application.save_new.save_new_command import SaveNewCommand
from domain.new.new_discovered_event import NewDiscoveredEvent
from domain.new.new_repository import NewRepository


class NewDiscoveredEventConsumer(EventConsumer):
    def __init__(self, new_repository: NewRepository, command_bus: CommandBus):
        self.__new_repository = new_repository
        self.__command_bus = command_bus

    def consume(self, event: NewDiscoveredEvent) -> None:
        existing_new = self.__new_repository.find_by_title(event.title)
        if existing_new is not None:
            return

        self.__command_bus.transport(self.__create_command_from_event(event))

    def __create_command_from_event(self, event: NewDiscoveredEvent) -> SaveNewCommand:
        return SaveNewCommand(
            title=event.title,
            url=event.url,
            content=event.content,
            source=event.source,
            date=event.date,
            language=event.language,
            hydrated=False,
            entities=[],
            summary=None,
            sentiment=None,
            image=event.image,
        )

    @classmethod
    def bus_stop_name(cls) -> str:
        return "event_consumer.news_manager.save_new.new_discovered"
