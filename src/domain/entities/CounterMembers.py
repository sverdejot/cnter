from typing import (
    final,
    Set,
    List,
    Type
)

from ..value_objects import UserId


@final
class CounterMembers:
    __value: Set[Type[UserId]]

    def __init__(self, members: List[Type[UserId]] = []):
        self.__value = set(members)

    @property
    def value(self):
        return self.__value

    def add(self, userId: UserId) -> None:
        self.__value.add(userId)
    
    def remove(self, userId: UserId) -> None:
        self.__value.remove(userId)

    def __eq__(self, other):
        if not (isinstance(other, type(self))):
            return False
        return (self.__value | other.value) > 0
