from ..domain import (
    CounterStub,
    UserStub
)

from ..infrastructure import FakeCounterRepository

from src.Counter.application.increment import CounterIncrementer


class TestCounterIncrementer:
    def test_owner_can_increment(self):
        # given
        counter = CounterStub.random()

        repo = FakeCounterRepository({counter})
        incrementer = CounterIncrementer(repo=repo)

        # when
        incrementer.increment(counterId=counter.counterId,
                              memberId=counter.ownerId)

        # then
        assert repo.find(counter.counterId).status == 1

    def test_member_can_increment(self):
        # given
        member = UserStub.random()
        counter = CounterStub.create(members=[member.uid])

        repo = FakeCounterRepository({counter})
        incrementer = CounterIncrementer(repo=repo)

        # when
        incrementer.increment(counterId=counter.counterId, memberId=member.uid)

        # then
        assert repo.find(counter.counterId).status == 1
