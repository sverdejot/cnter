from typing import (
    Type,
    final
)

from ..value_objects.CounterId import CounterId
from ..value_objects.UserId import UserId
from ..value_objects.CounterStatus import CounterStatus
from ..value_objects.CounterPrivate import CounterPrivate
from .CounterMembers import CounterMembers


@final
class Counter:
    __counterId: CounterId
    __ownerId: UserId
    __status: CounterStatus
    __private: CounterPrivate
    __members: CounterMembers

    def __init__(self,
                 counterId: CounterId,
                 ownerId: UserId,
                 status: CounterStatus,
                 private: CounterPrivate,
                 members: CounterMembers):
        self.__counterId = counterId
        self.__ownerId = ownerId
        self.__status = status
        self.__private = private
        self.__members = members

    @property
    def counterId(self):
        return self.__counterId

    @property
    def ownerId(self):
        return self.__ownerId

    @property
    def status(self):
        return self.__status.value

    @property
    def private(self):
        return self.__private.value

    @property
    def members(self):
        return self.__members

    @classmethod
    def create(cls, counterId: CounterId, ownerId: UserId, private: CounterPrivate) -> Type['Counter']:
        # Not the same instantiate as create new one
        return Counter(counterId=counterId,
                       ownerId=ownerId,
                       status=CounterStatus(0),
                       private=private,
                       members=CounterMembers([ownerId]))

    def increment(self, memberId: UserId) -> None:
        if memberId not in self.members:
            return
        # domain event increment
        self.__increment()

    def __increment(self) -> None:
        self.__status = CounterStatus(self.status + 1)

    def join(self, userId: UserId) -> None:
        if userId in self.members or self.private:
            return
        self.__members.add(userId)

    def kick(self, ownerId: UserId, memberId: UserId) -> None:
        if self.ownerId != ownerId:
            return
        self.__remove_member(memberId)
    
    def leave(self, memberId: UserId) -> None:
        self.__remove_member(memberId)

    def __remove_member(self, memberId: UserId) -> None:
        if not memberId in self.members:
            return
        self.__members.remove(memberId)
        
    def __hash__(self):
        return hash(self.counterId)

    def __eq__(self, other):
        if not (isinstance(other, type(self))):
            return False
        return (self.counterId == other.counterId)
