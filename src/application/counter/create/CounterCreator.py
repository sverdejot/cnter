from ....domain.repositories.CounterRepository import CounterRepository

from ....domain.entities import Counter

from ....domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)


class CounterCreator:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def create(self, counterId: CounterId, ownerId: UserId, private: CounterPrivate) -> None:
        counter = Counter.create(counterId=counterId, ownerId=ownerId, private=private)

        self.repo.add(counter)