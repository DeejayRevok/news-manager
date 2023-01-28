from dataclasses import dataclass
from typing import Optional

from bus_station.event_terminal.event import Event


@dataclass(frozen=True)
class NewDiscoveredEvent(Event):
    title: str
    url: str
    content: str
    source: str
    date: float
    language: str
    image: Optional[str] = None

    @classmethod
    def passenger_name(cls) -> str:
        return "event.new_discovered"
