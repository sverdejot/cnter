from typing import (
    Set,
    Optional
)

from src.contexts.Counter.domain.entities import (
    Counter
)

from src.contexts.Counter.domain.value_objects import (
    CounterId
)

class FakeCounterRepository:
    counters: Set[Counter]

    def __init__(self, counters: Optional[Set[Counter]] = set()):
        self.counters = counters

    async def add(self, counter: Counter) -> None:
        self.counters.add(counter)

    async def delete(self, counter: Counter) -> None:
        self.counters.remove(counter)

    async def find(self, counterId: CounterId) -> Optional[Counter]:
        return next((counter for counter in self.counters if counter.counterId == counterId), None)

    async def search(self, counterId: CounterId) -> Counter:
        return next(counter for counter in self.counters if counter.counterId == counterId)

    async def save(self, counter: Counter) -> None:
        pass