from uuid import (
    UUID,
    uuid4
)

from random import choice

from typing import List

from src.domain.entities import (
    Counter,
    User,
    CounterMembers
)

from src.domain.value_objects import (
    CounterId,
    UserId,
    CounterStatus,
    CounterPrivate,
)

class CounterStub:
    def __new__(cls, counterId: UUID = uuid4(),
                    ownerId: UUID = uuid4(),
                    status: int = 0,
                    private: bool = choice((True, False)),
                    members: List = []):
        return Counter(
                    counterId=CounterId(counterId), 
                    ownerId=UserId(ownerId),
                    status=CounterStatus(status),
                    private=CounterPrivate(private), 
                    members=CounterMembers(members)
                )

class UserStub:
    def __new__(cls, userId: UUID = uuid4()):
        return User(userId=UserId(userId))