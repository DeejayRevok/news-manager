from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class NamedEntity:
    text: str
    type: str
