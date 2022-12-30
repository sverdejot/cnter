from ...domain.entities import Counter

from ...domain.value_objects import (
    UserId
)


class CounterService:
    # i'll all of these as static method
    # as by now i don't have any property for any service
    
    # the purpose of these service is orchestrate between domain model
    # rather than orchestrate the use case (including interacting with repos)
    @staticmethod
    def increment(counter: Counter, memberId: UserId) -> None:
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
