from ..domain import (
    UserStub,
    CounterStub
)

from ..infrastructure import FakeCounterRepository

from src.contexts.Counter.application.leave import CounterLeaver


class TestCounterLeaver:
    def test_member_can_leave(self):
        # given
        member = UserStub.random()
        counter = CounterStub.create(members=[member.uid])

        repo = FakeCounterRepository({counter})
        leaver = CounterLeaver(repo=repo)

        # when
        leaver(counterId=counter.counterId, memberId=member.uid)

        # then
        assert member.uid not in repo.search(counter.counterId).members
