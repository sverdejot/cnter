from ...domain.entities import Counter

from ...domain.value_objects import (
    UserId
)


class CounterService:
    @staticmethod
    def increment(counter: Counter, memberId: UserId) -> None:
        print({memberId})
        print(counter.members.value)
        if memberId not in counter.members:
            return
        # domain event increment
        counter.increment()
    
    @staticmethod
    def join(counter: Counter, userId: UserId) -> None:
        if userId in counter.members or counter.private:
            return
        counter.join(userId)
    
    @staticmethod
    def kick(counter: Counter, ownerId: UserId, memberId: UserId) -> None:
        if counter.ownerId != ownerId:
            return
        counter.leave(memberId)

    @staticmethod
    def leave(counter: Counter, memberId: UserId) -> None:
        counter.leave(memberId)
