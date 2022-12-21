from ....domain.repositories.CounterRepository import CounterRepository

from ....domain.entities import Counter

from ....domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)

class CounterLeaver:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def leave(self, counterId: CounterId, userId: UserId):
        counter = repo.find(counterId)
        
        counter.leave(userId)