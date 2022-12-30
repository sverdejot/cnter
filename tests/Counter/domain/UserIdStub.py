from uuid import (
    UUID,
    uuid4
)

from typing import Optional

from src.contexts.Counter.domain.value_objects import UserId


class UserIdStub:
    @staticmethod
    def create(userId: Optional[UUID] = None) -> UserId:
        return UserId(userId or uuid4())

    @classmethod
    def random(cls) -> UserId:
        return cls.create()
