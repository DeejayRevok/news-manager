from logging import Logger

from bus_station.command_terminal.command_handler import CommandHandler
from bus_station.event_terminal.bus.event_bus import EventBus

from application.save_new.save_new_command import SaveNewCommand
from domain.new.new import New
from domain.new.new_repository import NewRepository
from domain.new.new_saved_event import NewSavedEvent


class SaveNewCommandHandler(CommandHandler):
    def __init__(self, new_repository: NewRepository, event_bus: EventBus, logger: Logger):
        self.__new_repository = new_repository
        self.__event_bus = event_bus
        self.__logger = logger

    def handle(self, command: SaveNewCommand) -> None:
        self.__logger.info("Starting saving new")

        self.__new_repository.save(self.__create_new_from_command(command))
        self.__event_bus.transport(self.__create_event_from_command(command))

        self.__logger.info("Finished saving new")

    def __create_new_from_command(self, command: SaveNewCommand) -> New:
        return New(
            title=command.title,
            url=command.url,
            content=command.content,
            source=command.source,
            date=command.date,
            language=command.language,
            hydrated=command.hydrated,
            entities=command.entities,
            summary=command.summary,
            sentiment=command.sentiment,
            image=command.image,
        )

    def __create_event_from_command(self, command: SaveNewCommand) -> NewSavedEvent:
        return NewSavedEvent(
            title=command.title,
            url=command.url,
            content=command.content,
            source=command.source,
            date=command.date,
            language=command.language,
            hydrated=command.hydrated,
            entities=command.entities,
            summary=command.summary,
            sentiment=command.sentiment,
            image=command.image,
        )

    @classmethod
    def bus_stop_name(cls) -> str:
        return "command_handler.news_manager.save_new"
