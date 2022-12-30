from src.contexts.Counter.domain.entities import Counter
from src.contexts.Counter.domain.repositories import CounterRepository
from src.contexts.Counter.domain.value_objects import CounterId

from typing import Optional


class MondoDBCounterRepository(CounterRepository):
    def add(self, counter: Counter) -> None:
        pass

    def delete(self, counter: Counter) -> None:
        pass

    def find(self, counterId: CounterId) -> Counter:
        pass

    def search(self, counterId: CounterId) -> Optional[Counter]:
        pass