from ....domain.entities import (
    Counter,
    CounterMembers
)
from ....domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate,
    CounterStatus
)

from uuid import UUID

from motor.core import ClientSession

class MotorCounterRepository:
    def __init__(self, session: ClientSession):
        self.__session = session

    async def add(self, counter: Counter) -> None:
        counters_collection = self.__session.client.counter.counters
        async with self.__session.start_transaction():
            counters_collection.insert_one(document={
                'counterId': str(counter.counterId),
                'ownerId': str(counter.ownerId),
                'private': counter.private,
                'status': counter.status,
                'members': [str(counter.ownerId)]
            })

    def delete(self, counterId: CounterId) -> None:
        pass

    async def find(self, counterId: CounterId) -> Counter | None:
        counters_collection = self.__session.client.counter.counters
        async with self.__session.start_transaction() as tx:
            counter = await counters_collection.find_one({'counterId': str(counterId)})

            return Counter(
                counterId=CounterId(counter['counterId']),
                ownerId=UserId(counter['ownerId']),
                status=CounterStatus(counter['status']),
                private=CounterPrivate(counter['private']),
                members=CounterMembers([UserId(UUID(member)) for member in counter['members']])
            )

    async def save(self, counter: Counter) -> None:
        counters_collection = self.__session.client.counter.counters
        async with self.__session.start_transaction() as tx:
            await counters_collection.update_one(
                filter={'counterId': str(counter.counterId)},
                update={
                    '$set':
                        {
                            'ownerId': str(counter.ownerId.value),
                            'private': counter.private,
                            'status': counter.status,
                            'members': [
                                str(member) for member in counter.members
                            ]
                        }
                }
            )