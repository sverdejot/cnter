from uuid import (
    UUID,
    uuid4
)

from typing import (
    Optional
)

from src.Counter.domain.entities import (
    User,
)

from src.Counter.domain.value_objects import (
    UserId
)


class UserStub:
    @staticmethod
    def create(userId: Optional[UUID] = None) -> User:
        return User(userId=UserId(userId or uuid4()))

    @classmethod
    def random(cls) -> User:
        return cls.create()
