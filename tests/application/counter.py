from uuid import uuid4

from src.domain.entities.Counter import (
    Counter,
    User,
    CounterMembers
)

from src.domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate,
    CounterStatus
)

from src.domain.repositories.CounterRepository import CounterRepository

from src.application.counter.create.counter import CounterCreator


class FakeCounterRepository(CounterRepository):
    def __init__(self, counters=[]):
        self.counters = counters

    def add(self, counter: Counter):
        self.counters.append(counter)

    def delete(self, counter: Counter):
        pass

    def find(self, counterId: CounterId) -> Counter:
        return next((counter for counter in self.counters if counter.counterId == counterId))


def test_counter_creator_can_create_members():
    counterId = CounterId(uuid4())
    ownerId = UserId(uuid4())
    private = CounterPrivate(False)

    counter = Counter.create(
        counterId=counterId, ownerId=ownerId, private=private)

    fakeRepo = FakeCounterRepository()
    counterCreator = CounterCreator(fakeRepo)

    counterCreator.create(counterId=counterId,
                          ownerId=ownerId, private=private)
    
    print(fakeRepo.counters)
    assert fakeRepo.find(counterId) == counter
