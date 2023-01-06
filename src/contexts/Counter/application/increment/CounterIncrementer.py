from ...domain.repositories.CounterRepository import CounterRepository

from ...domain.services import CounterService

from ...domain.entities import Counter

from ...domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)


class CounterIncrementer:
    repo: CounterRepository
    service: CounterService

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    async def __call__(self, counterId: CounterId, memberId: UserId) -> None:
        counter = await self.repo.search(counterId)

        CounterService.increment(counter=counter, memberId=memberId)

        await self.repo.save(counter)