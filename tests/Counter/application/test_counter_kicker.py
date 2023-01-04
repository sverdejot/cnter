from ..domain import (
    CounterStub,
    UserStub
)

from ..infrastructure import FakeCounterRepository

from src.contexts.Counter.application.kick import CounterKicker


class TestCounterKicker:
    def test_owner_can_kick_member(self):
        # given
        owner = UserStub.random()
        member = UserStub.random()

        counter = CounterStub.create(
            ownerId=owner.uid.value, members=[member.uid])

        repo = FakeCounterRepository({counter})
        kicker = CounterKicker(repo=repo)

        # when
        kicker(ownerId=owner.uid, counterId=counter.counterId,
                    memberId=member.uid)

        # then
        assert member.uid not in repo.find(counterId=counter.counterId).members

    def test_member_cannot_kick_another_member(self):
        # given
        member = UserStub.random()
        another_member = UserStub.random()

        counter = CounterStub.create(members=[member.uid, another_member.uid])

        repo = FakeCounterRepository({counter})
        kicker = CounterKicker(repo=repo)

        # when
        kicker(ownerId=member.uid, counterId=counter.counterId,
                    memberId=another_member.uid)

        # then
        assert another_member.uid in repo.find(counter.counterId).members
