from uuid import uuid4

from ..domain import (
    UserIdStub,
    CounterIdStub,
    CounterPrivateStub,
    CounterStub
)

from src.Counter.application.create import CounterCreator

from ..infrastructure import FakeCounterRepository


class TestCounterCreator:
    # it shouldn't create a counter for a non existing user
    # so a validation of existing user must be implemented
    # i'd give it a thought
    def test_can_create_counter(self):
        # given
        counter = CounterStub.random()

        counterId = counter.counterId
        ownerId = counter.ownerId
        private = counter.private

        repo = FakeCounterRepository()
        creator = CounterCreator(repo=repo)

        # when
        creator.create(counterId=counterId, ownerId=ownerId, private=private)

        # then
        assert counter == repo.find(counterId)
