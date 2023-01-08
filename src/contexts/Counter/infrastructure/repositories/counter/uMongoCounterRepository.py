from ....domain.entities import (
    Counter,
)
from ....domain.value_objects import (
    CounterId
)

from ....domain.exceptions import NotFoundException

from Counter.infrastructure.odm.counter.documents.counter import Counter as CounterDocument

class uMongoCounterRepository:
    async def add(self, counter: Counter) -> None:
        await CounterDocument.fromModel(counter, created=False).commit()

    async def delete(self, counterId: CounterId) -> None:
        if counter_document:=CounterDocument.find_one({'_id': counterId.value}):
            counter_document.delete()
            await counter_document.commit()

    async def find(self, counterId: CounterId) -> Counter | None:
        c = await CounterDocument.find_one({'_id': counterId.value})
        print(c)
        return c.toModel()

    async def search(self, counterId: CounterId) -> Counter:
        if not (counter:=await CounterDocument.find_one({'_id': counterId.value})):
            raise NotFoundException
        print(counter)
        return counter.toModel()

    async def save(self, counter: Counter) -> None:
        await CounterDocument.fromModel(counter).commit()
