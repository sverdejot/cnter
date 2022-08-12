from ..abstract import AbstractUnitOfWork

from cnter.core.adapters.repository.counter import SQLCounterRepository
from cnter.core.adapters.repository.user import SQLUserRepository

from cnter.core.adapters.message import bus

from cnter.config.db import engine

from sqlalchemy.orm import sessionmaker

SESSION_FACTORY = sessionmaker(bind=engine)

class SQLUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.counters = SQLCounterRepository(self.session)
        self.users = SQLUserRepository(self.session)

    def commit(self):
        return self.session.commit()
    
    def rollback(self):
        return self.session.rollback()

    def publish_events(self):
        for counter in self.counters.seen():
            events = iter(counter.events)
            while event := next(events, None):
                bus.handle(event)

        for user in self.users.seen():
            events = iter(user.events)
            while event := next(events, None):
                bus.handle(event)
        