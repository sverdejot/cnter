from ...domain.repositories.CounterRepository import CounterRepository

from ...domain.entities import Counter

from ...domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)

from asyncio import Task


class CounterCreator:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    async def __call__(self, counterId: CounterId, ownerId: UserId, private: CounterPrivate) -> Task:
        counter = Counter.create(
            counterId=counterId, 
            ownerId=ownerId, 
            private=private
        )

        await self.repo.add(counter)
