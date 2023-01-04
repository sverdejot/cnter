from ....domain.entities import Counter, CounterMembers

from ....domain.value_objects import (
    CounterId,
    UserId,
    CounterStatus,
    CounterPrivate
)

from typing import Optional

from uuid import UUID

from boto3.dynamodb.table import TableResource

class DynamoDBCounterRepository:
    def __init__(self, table: TableResource):
        self.__table = table

    def add(self, counter: Counter) -> None:
        self.__table.put_item(Item={
            'counterId': str(counter.counterId),
            'ownerId': str(counter.ownerId),
            'status': counter.status,
            'private': counter.private,
        })

    def delete(self, counter: Counter) -> None:
        self.__table.delete_item(Key={
            'counterId': str(counter.counterId)
        })

    def find(self, counterId: CounterId) -> Counter:
        item = self.__table.get_item(Key={
            'counterId': str(counterId.value)
        }).get('Item')
        
        return Counter(
            counterId=CounterId(value=item['counterId']),
            ownerId=UserId(value=item['ownerId']),
            status=CounterStatus(value=item['status']),
            private=CounterPrivate(value=item['private']),
            members=CounterMembers({})
        )

    def search(self, counterId: CounterId) -> Optional[Counter]:
        return self.find(counterId=counterId)