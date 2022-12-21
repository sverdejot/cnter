from uuid import uuid4

from src.domain.entities.Counter import (
    Counter,
    CounterMembers
)

from src.domain.value_objects import (
    CounterId,
    UserId,
    CounterPrivate
)

from .stubs import (
    CounterStub,
    UserStub
)


class TestCounter:
    def test_counter_can_create(self):
        counterId = CounterId(uuid4())
        ownerId = UserId(uuid4())
        private = CounterPrivate(False)

        counter = Counter.create(counterId=counterId, ownerId=ownerId, private=private)

        assert counter.counterId == counterId.value
        assert counter.ownerId == ownerId.value
        assert counter.status == 0
        assert counter.private == private.value
    
    def test_member_can_increment(self):
        member = UserStub()
        counter = CounterStub(members=[member.uid])

        counter.increment(memberId=member.uid)

        assert counter.status == 1

    def test_owner_can_kick_member(self):
        owner = UserStub()
        member = UserStub()
        counter = CounterStub(ownerId=owner.uid, members=[member.uid])

        counter.kick(ownerId=owner.uid, memberId=member.uid)

        assert member not in counter.members

    def test_member_can_leaver_counter(self):
        member = UserStub()
        counter = CounterStub(members=[member.uid])

        counter.leave(memberId=member.uid)