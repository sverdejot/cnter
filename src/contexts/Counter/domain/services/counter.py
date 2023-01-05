from ...domain.entities import Counter

from ...domain.value_objects import (
    UserId
)

from ..exceptions import (
    AlreadyMemberException,
    UnauthorizedException,
    PrivateException
)

class CounterService:
    @staticmethod
    def increment(counter: Counter, memberId: UserId) -> None:
        if memberId not in counter.members:
            raise UnauthorizedException
        # domain event increment
        counter.increment()
    
    @staticmethod
    def join(counter: Counter, userId: UserId) -> None:
        if member:=(userId in counter.members) or counter.private:
            raise AlreadyMemberException if member else PrivateException
        counter.join(userId)
    
    @staticmethod
    def kick(counter: Counter, ownerId: UserId, memberId: UserId) -> None:
        if counter.ownerId != ownerId:
            raise UnauthorizedException
        counter.leave(memberId)

    @staticmethod
    def leave(counter: Counter, memberId: UserId) -> None:
        counter.leave(memberId)
