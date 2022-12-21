from typing import (
    final,
    Type
)

from ..value_objects import UserId

@final
class User:
    userId: UserId

    @property
    def uid(self):
        return self.userId

    def __init__(self, userId: UserId):
        self.userId = userId

    def create(self, userId: UserId) -> Type['User']:
        return User(userId=userId)

    def __eq__(self, other) -> bool:
        if not (isinstance(other, type(self))):
            return False
        return self.userId == other.userId
    
    def __hash__(self):
        return hash(self.userId)
