from uuid import (
    UUID,
    uuid4
)

from random import choice

from typing import (
    List,
    Optional
)

from src.Counter.domain.entities import (
    Counter,
    CounterMembers
)

from src.Counter.domain.value_objects import (
    CounterId,
    UserId,
    CounterStatus,
    CounterPrivate,
)


class CounterStub:
    @staticmethod
    def create(counterId: Optional[UUID] = None,
               ownerId: Optional[UUID] = None,
               status: int = 0,
               private: Optional[bool] = None,
               members: List = []) -> Counter:
        counterId = CounterId(counterId or uuid4())
        ownerId = UserId(ownerId or uuid4())
        status = CounterStatus(status)
        private = CounterPrivate(private or choice((True, False)))
        members = CounterMembers(members + [ownerId])

        return Counter(counterId, ownerId, status, private, members)

    @classmethod
    def random(cls):
        return cls.create()