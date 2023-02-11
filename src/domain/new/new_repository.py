from abc import abstractmethod
from typing import Protocol, Optional, Iterable

from domain.new.find_news_criteria import FindNewsCriteria
from domain.new.new import New


class NewRepository(Protocol):
    @abstractmethod
    def save(self, new: New) -> None:
        pass

    @abstractmethod
    def find_by_title(self, title: str) -> Optional[New]:
        pass

    @abstractmethod
    def find_by_criteria(self, criteria: FindNewsCriteria) -> Iterable[New]:
        pass
