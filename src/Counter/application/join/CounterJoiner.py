from ...domain.repositories.CounterRepository import CounterRepository

from ...domain.services import CounterService

from ...domain.value_objects import (
    CounterId,
    UserId
)


class CounterJoiner:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def join(self, counterId: CounterId, userId: UserId) -> None:
        counter = self.repo.search(counterId)

        CounterService.join(counter=counter, userId=userId)