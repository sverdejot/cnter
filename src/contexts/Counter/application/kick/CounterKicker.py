from ...domain.repositories.CounterRepository import CounterRepository

from ...domain.services import CounterService

from ...domain.entities import Counter

from ...domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)

class CounterKicker:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def __call__(self, ownerId: UserId, counterId: CounterId, memberId: UserId):
        counter = self.repo.search(counterId)

        CounterService.kick(counter=counter, ownerId=ownerId, memberId=memberId)