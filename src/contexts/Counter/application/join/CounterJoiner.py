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

    async def __call__(self, counterId: CounterId, userId: UserId) -> None:
        counter = await self.repo.search(counterId)

        CounterService.join(counter=counter, userId=userId)

        await self.repo.save(counter)