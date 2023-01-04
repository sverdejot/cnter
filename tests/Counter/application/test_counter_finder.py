from ..domain import CounterStub
from ..infrastructure import FakeCounterRepository

from Counter.application.find import CounterFinder

class TestCounterFinder:
    def test_can_find_counter(self):
        # given
        counter = CounterStub.random()

        repo = FakeCounterRepository({counter})
        finder = CounterFinder(repo)

        # when
        returned_counter = finder(counterId=counter.counterId)

        # then
        assert returned_counter == counter

