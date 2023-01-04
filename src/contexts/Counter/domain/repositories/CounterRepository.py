from typing import (
    Optional,
    Protocol
)

from ..entities import Counter

from ..value_objects import CounterId


class CounterRepository(Protocol):
    def add(self, counter: Counter) -> None:
        ...

    def delete(self, counter: Counter) -> None:
        ...

    def find(self, counterId: CounterId) -> Counter:
        ...

    def search(self, counterId: CounterId) -> Optional[Counter]:
        ...
