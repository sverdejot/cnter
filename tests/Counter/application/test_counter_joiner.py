from ..domain import (
    CounterStub,
    UserStub
)

from ..infrastructure import FakeCounterRepository

from src.Counter.application.join import CounterJoiner


class TestCounterJoiner:
    # TODO: flaky one, must give it a check
    def test_user_can_join_public_counter(self):
        # given
        counter = CounterStub.create(private=False)
        user = UserStub.random()

        repo = FakeCounterRepository({counter})
        joiner = CounterJoiner(repo=repo)

        # when
        joiner.join(counterId=counter.counterId, userId=user.uid)

        # then
        assert user.uid in repo.find(counter.counterId).members
