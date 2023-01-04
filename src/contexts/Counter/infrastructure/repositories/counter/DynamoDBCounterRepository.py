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
    def __init__(self, counters: TableResource | None = None, members: TableResource | None = None):
        self.__counters = counters
        self.__members = members

    def add(self, counter: Counter) -> None:
        self.__counters.put_item(Item={
            'counterId': str(counter.counterId),
            'ownerId': str(counter.ownerId),
            'status': counter.status,
            'private': counter.private,
        })
        self.__members.put_item(Item={
            'counterId': str(counter.counterId),
            'members': set({counter.ownerId})
        })

    def delete(self, counter: Counter) -> None:
        self.__counters.delete_item(Key={
            'counterId': str(counter.counterId)
        })
        self.__members.delete_item(Key={
            'counterId': str(counter.counterId)
        })

    def find(self, counterId: CounterId) -> Counter:
        item = self.__counters.get_item(Key={
            'counterId': str(counterId)
        }).get('Item')

        members = self.__members.get_item(Key={
            'counterId': str(counterId)
        }).get('Item').get('members')
        
        return Counter(
            counterId=CounterId(value=item['counterId']),
            ownerId=UserId(value=item['ownerId']),
            status=CounterStatus(value=item['status']),
            private=CounterPrivate(value=item['private']),
            members=CounterMembers([members])
        )

    def search(self, counterId: CounterId) -> Optional[Counter]:
        return self.find(counterId=counterId)