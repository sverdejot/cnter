from ....domain.repositories.CounterRepository import CounterRepository

from ....domain.entities import Counter

from ....domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)


class CounterJoiner:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def join(counter: CounterId, userId: UserId):
        counter = self.repo.find(counterId)

        counter.join(userId)