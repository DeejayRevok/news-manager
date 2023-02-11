from dataclasses import dataclass, field
from typing import List, Optional

from bus_station.event_terminal.event import Event

from domain.new.named_entity import NamedEntity


@dataclass(frozen=True)
class NewHydratedEvent(Event):
    title: str
    url: str
    content: str
    source: str
    date: float
    language: str
    hydrated: bool = False
    entities: List[NamedEntity] = field(default_factory=list)
    summary: Optional[str] = None
    sentiment: Optional[float] = None
    image: Optional[str] = None

    @classmethod
    def passenger_name(cls) -> str:
        return "event.new_hydrated"
