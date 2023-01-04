from typing import (
    Protocol
)

from ..entities import User
from ..value_objects import UserId


class UserRepository(Protocol):
    def create(self, user: User) -> None:
        ...

    def find(self, userId: UserId) -> User:
        ...
