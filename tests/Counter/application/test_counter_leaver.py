from ..domain import (
    UserStub,
    CounterStub
)

from ..fakes import FakeCounterRepository

from src.contexts.Counter.application.leave import CounterLeaver

import pytest

class TestCounterLeaver:
    @pytest.mark.asyncio
    async def test_member_can_leave(self):
        # given
        member = UserStub.random()
        counter = CounterStub.create(members=[member.uid])

        repo = FakeCounterRepository({counter})
        leaver = CounterLeaver(repo=repo)

        # when
        await leaver(counterId=counter.counterId, memberId=member.uid)

        # then
        returned_counter = await repo.search(counter.counterId)
        assert member.uid not in returned_counter.members
