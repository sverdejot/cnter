from typing import (
    Set,
    Optional
)

from src.Counter.domain.entities import (
    Counter
)

from src.Counter.domain.value_objects import (
    CounterId
)

from src.Counter.domain.repositories import CounterRepository


class FakeCounterRepository(CounterRepository):
    counters: Set[Counter]

    def __init__(self, counters: Optional[Set[Counter]] = set()):
        self.counters = counters

    def add(self, counter: Counter) -> None:
        self.counters.add(counter)

    def delete(self, counter: Counter) -> None:
        self.counters.remove(counter)

    def find(self, counterId: CounterId) -> Optional[Counter]:
        return next((counter for counter in self.counters if counter.counterId == counterId), None)

    def search(self, counterId: CounterId) -> Counter:
        return next(counter for counter in self.counters if counter.counterId == counterId)
