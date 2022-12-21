from ....domain.repositories.CounterRepository import CounterRepository

from ....domain.entities import Counter

from ....domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)

class CounterKicker:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def kick(self, ownerId: UserId, counterId: CounterId, memberId: memberId):
        counter = self.repo.find(counterId)

        counter.kick(ownerId, memberId)