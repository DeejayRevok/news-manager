from bus_station.command_terminal.command_handler_registry import CommandHandlerRegistry
from yandil.container import default_container

from application.save_new.save_new_command_handler import SaveNewCommandHandler


def register() -> None:
    registry = default_container[CommandHandlerRegistry]
    registry.register(default_container[SaveNewCommandHandler])
