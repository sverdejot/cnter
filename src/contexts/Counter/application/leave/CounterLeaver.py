from ...domain.repositories.CounterRepository import CounterRepository

from ...domain.services import CounterService

from ...domain.entities import Counter

from ...domain.value_objects import (
    CounterId,
    UserId,
)


class CounterLeaver:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def __call__(self, counterId: CounterId, memberId: UserId):
        counter = self.repo.search(counterId)

        CounterService.leave(counter=counter, memberId=memberId)