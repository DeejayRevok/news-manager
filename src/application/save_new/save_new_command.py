from dataclasses import dataclass
from typing import List, Optional

from bus_station.command_terminal.command import Command

from domain.new.named_entity import NamedEntity


@dataclass(frozen=True)
class SaveNewCommand(Command):
    title: str
    url: str
    content: str
    source: str
    date: float
    language: str
    hydrated: bool
    entities: List[NamedEntity]
    summary: Optional[str]
    sentiment: Optional[float]
    image: Optional[str]

    @classmethod
    def passenger_name(cls) -> str:
        return "command.news_manager.save_new"