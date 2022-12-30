from uuid import (
    UUID,
    uuid4
)

from src.contexts.Counter.domain.value_objects import CounterId


class CounterIdStub:
    @staticmethod
    def create(counterId: UUID = None) -> CounterId:
        return CounterId(counterId or uuid4())

    @classmethod
    def random(cls) -> CounterId:
        return cls.create()
