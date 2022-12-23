from ...domain.repositories.CounterRepository import CounterRepository

from ...domain.entities import Counter

from ...domain.value_objects import (
    CounterId,
    UserId,
)


class CounterLeaver:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def leave(self, counterId: CounterId, memberId: UserId):
        counter = self.repo.search(counterId)

        counter.leave(memberId)
