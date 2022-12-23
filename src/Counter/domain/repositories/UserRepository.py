from abc import (
    ABCMeta,
    abstractmethod
)

from typing import (
    List
)

from ..entities import User
from ..value_objects import UserId


class UserRepository(metaclass=ABCMeta):
    users: List[User]

    @abstractmethod
    def create(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def find(self, userId: UserId) -> User:
        raise NotImplementedError
