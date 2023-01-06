from ..domain import (
    CounterStub,
    UserStub
)

from ..fakes import FakeCounterRepository

from src.contexts.Counter.application.increment import CounterIncrementer

import pytest


class TestCounterIncrementer:
    @pytest.mark.asyncio
    async def test_owner_can_increment(self):
        # given
        counter = CounterStub.random()

        repo = FakeCounterRepository({counter})
        incrementer = CounterIncrementer(repo=repo)

        # when
        await incrementer(counterId=counter.counterId,
                              memberId=counter.ownerId)

        # then
        returned_counter = await repo.find(counter.counterId)
        assert returned_counter.status == 1

    @pytest.mark.asyncio
    async def test_member_can_increment(self):
        # given
        member = UserStub.random()
        counter = CounterStub.create(members=[member.uid])

        repo = FakeCounterRepository({counter})
        incrementer = CounterIncrementer(repo=repo)

        # when
        await incrementer(counterId=counter.counterId, memberId=member.uid)

        # then
        returned_counter = await repo.find(counter.counterId)
        assert returned_counter.status == 1
