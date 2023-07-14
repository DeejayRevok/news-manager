from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class NewDiscoveredEvent:
    title: str
    url: str
    content: str
    source: str
    date: float
    language: str
    image: Optional[str] = None
