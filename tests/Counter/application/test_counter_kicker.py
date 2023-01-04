from ..domain import (
    CounterStub,
    UserStub
)

from ..infrastructure import FakeCounterRepository

from src.contexts.Counter.application.kick import CounterKicker

import pytest


class TestCounterKicker:
    @pytest.mark.asyncio
    async def test_owner_can_kick_member(self):
        # given
        owner = UserStub.random()
        member = UserStub.random()

        counter = CounterStub.create(
            ownerId=owner.uid.value, members=[member.uid])

        repo = FakeCounterRepository({counter})
        kicker = CounterKicker(repo=repo)

        # when
        await kicker(ownerId=owner.uid, counterId=counter.counterId,
                    memberId=member.uid)

        # then
        returned_counter = await repo.find(counterId=counter.counterId)
        assert member.uid not in returned_counter.members

    @pytest.mark.asyncio
    async def test_member_cannot_kick_another_member(self):
        # given
        member = UserStub.random()
        another_member = UserStub.random()

        counter = CounterStub.create(members=[member.uid, another_member.uid])

        repo = FakeCounterRepository({counter})
        kicker = CounterKicker(repo=repo)

        # when
        await kicker(ownerId=member.uid, counterId=counter.counterId,
                    memberId=another_member.uid)

        # then
        returned_counter = await repo.find(counter.counterId)
        assert another_member.uid in returned_counter.members
