from ....domain.repositories.CounterRepository import CounterRepository

from ....domain.entities import Counter

from ....domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)


class CounterIncrementer:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def increment(self, counterId: CounterId)