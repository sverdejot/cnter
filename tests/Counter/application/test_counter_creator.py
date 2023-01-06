from uuid import uuid4

from ..domain import (
    UserIdStub,
    CounterIdStub,
    CounterPrivateStub,
    CounterStub
)

from src.contexts.Counter.application.create import CounterCreator

from ..fakes import FakeCounterRepository

import pytest



class TestCounterCreator:
    @pytest.mark.asyncio
    async def test_can_create_counter(self):
        # given
        counter = CounterStub.random()

        counterId = counter.counterId
        ownerId = counter.ownerId
        private = counter.private

        repo = FakeCounterRepository()
        creator = CounterCreator(repo=repo)

        # when
        await creator(counterId=counterId, ownerId=ownerId, private=private)

        # then
        assert counter == await repo.find(counterId)
