from typing import Optional

from random import choice

from src.Counter.domain.value_objects import CounterPrivate


class CounterPrivateStub:
    @staticmethod
    def create(private: Optional[bool] = None) -> CounterPrivate:
        return CounterPrivate(private or choice((True, False)))

    @classmethod
    def random(cls):
        return cls.create()