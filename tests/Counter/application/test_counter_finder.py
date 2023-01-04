from ..domain import CounterStub
from ..infrastructure import FakeCounterRepository

from Counter.application.find import CounterFinder

import pytest

class TestCounterFinder:
    @pytest.mark.asyncio
    async def test_can_find_counter(self):
        # given
        counter = CounterStub.random()

        repo = FakeCounterRepository({counter})
        finder = CounterFinder(repo)

        # when
        returned_counter = await finder(counterId=counter.counterId)

        # then
        assert returned_counter == counter

