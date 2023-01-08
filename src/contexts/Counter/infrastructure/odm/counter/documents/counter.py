from umongo import (
    fields,
    Document
)

from ...uMongoODM import instance

from .....domain.entities import (
    Counter as CounterModel, 
    CounterMembers as CounterMembersModel
)

from .....domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate,
    CounterStatus
)

@instance.register
class Counter(Document):
    _id = fields.UUIDField(required=True, unique=True)

    ownerId = fields.UUIDField(required=True)
    
    status = fields.IntegerField(default=0)

    private = fields.BooleanField()

    members = fields.ListField(fields.UUIDField)
        
    @classmethod
    def fromModel(cls, counter: CounterModel, created=True):
        counter_document = cls(
            _id=counter.counterId.value,
            ownerId=counter.ownerId.value,
            private=counter.private,
            status=counter.status,
            members=[memberId.value for memberId in counter.members],
        )
        counter_document.is_created = created
        return counter_document

    def toModel(self):
        return CounterModel(
            counterId=CounterId(self._id),
            ownerId=UserId(self.ownerId),
            status=CounterStatus(self.status),
            private=CounterPrivate(self.private),
            members=CounterMembersModel({UserId(member) for member in self.members})
        )
        
    class Meta():
        collection_name = 'counters'
        index = 'counterId'
