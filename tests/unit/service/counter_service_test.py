from cnter.core.domain.model import User, Counter

from cnter.core.service.uow.abstract import AbstractUnitOfWork
from cnter.core.adapters.repository.abstract import AbstractRepository

from cnter.core.service.services.counter import CounterService

class FakeUserRepository(AbstractRepository):
    def __init__(self, users=[]):
        self.users = set(users)
        super().__init__()

    def add(self, user: User):
        self.seen.add(user)
        return self._add(user)

    def get(self, username: str):
        if user := self._get(username):
            self.seen.add(user)
        return user

    def _add(self, user: User):
        self.users.add(user)

    def _get(self, username: str):
        return next(user for user in self.users if user.username == username) if self.users else None

class FakeCounterRepository(AbstractRepository):
    def __init__(self, counters=[]):
        self.counters = set(counters)
        super().__init__()

    def add(self, counter: Counter):
        self.seen.add(counter)
        return self._add(counter)

    def get(self, alias: str):
        if counter := self._get(alias):
            self.seen.add(counter)
        return counter

    def _add(self, counter: Counter):
        self.counters.add(counter)

    def _get(self, alias: str):
        return next(counter for counter in self.counters if counter.alias == alias) if self.counters else None

class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self, users, counters):
        self.commited = False
        self.users = FakeUserRepository(users)
        self.counters = FakeCounterRepository(counters)   
    
    def __enter__(self):
        pass

    def commit(self):
        self.commited = True

    def rollback(self):
        pass

    def publish_events(self):
        pass

def test_service_can_join_counter():
    user = User(username='test-user')
    owner = User(username='test-owner')
    counter = Counter(alias='test-alias', owner=owner)

    uow = FakeUnitOfWork(users=[user, owner], counters=[counter])

    counterService = CounterService()

    result = counterService.join(alias=counter.alias, username=user.username, uow=uow)

    assert result == True
    assert user in counter.members
    
