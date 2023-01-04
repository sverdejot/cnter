from ..domain import (
    CounterStub,
    UserStub
)

from ..infrastructure import FakeCounterRepository

from src.contexts.Counter.application.join import CounterJoiner

import pytest


class TestCounterJoiner:
    # TODO: flaky one, must give it a check
    @pytest.mark.asyncio
    async def test_user_can_join_public_counter(self):
        # given
        counter = CounterStub.create(private=False)
        user = UserStub.random()

        repo = FakeCounterRepository({counter})
        joiner = CounterJoiner(repo=repo)

        # when
        await joiner(counterId=counter.counterId, userId=user.uid)

        # then
        returned_counter = await repo.find(counter.counterId)
        assert user.uid in returned_counter.members
