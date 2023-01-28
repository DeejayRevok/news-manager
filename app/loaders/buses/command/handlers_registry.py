from bus_station.command_terminal.registry.command_registry import CommandRegistry
from pypendency.builder import container_builder


def register() -> None:
    registry: CommandRegistry = container_builder.get(
        "bus_station.command_terminal.registry.in_memory_command_registry.InMemoryCommandRegistry"
    )
    save_command_handler = container_builder.get(
        "application.save_new.save_new_command_handler.SaveNewCommandHandler"
    )
    registry.register(save_command_handler, save_command_handler)
