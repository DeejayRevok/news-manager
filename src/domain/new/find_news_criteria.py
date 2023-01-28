from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FindNewsCriteria:
    source: Optional[str]
    hydrated: Optional[bool]
    from_sentiment: Optional[float]
    to_sentiment: Optional[float]
    from_date: Optional[float]
    to_date: Optional[float]
