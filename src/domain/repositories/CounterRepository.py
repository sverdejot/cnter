from abc import (
    ABCMeta,
    abstractmethod,
)

from typing import (
    Type,
    List,
)

from ..entities import Counter


class CounterRepository(metaclass=ABCMeta):
    counters: List[Counter]

    @abstractmethod
    def add(self, counter) -> None:
        return

    @abstractmethod
    def delete(self, counter) -> None:
        return

    @abstractmethod
    def find(self, counterId) -> Counter:
        return