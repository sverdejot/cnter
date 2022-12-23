from abc import (
    ABCMeta,
    abstractmethod,
)

from typing import (
    Type,
    List,
    Optional
)

from ..entities import Counter


class CounterRepository(metaclass=ABCMeta):
    @abstractmethod
    def add(self, counter) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, counter) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(self, counterId) -> Counter:
        raise NotImplementedError

    @abstractmethod
    def search(self, counterId) -> Optional[Counter]:
        raise NotImplementedError
