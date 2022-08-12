from ast import Pass
from cnter.core.domain.model import Counter
from cnter.core.domain.model import User

from cnter.core.service.uow.abstract import AbstractUnitOfWork

class NonExisting(Exception):
    pass

class AlreadyExists(Exception):
    pass

class CounterService:
    def create(self, alias: str, owner_uname: str, uow: AbstractUnitOfWork):
        with uow:
            if not (owner:=uow.users.get(owner_uname)):
                raise NonExisting(f"User {owner_uname} does not exists")

            if uow.counters.get(alias):
                raise AlreadyExists(f"Counter {alias} already exists")
        
            uow.counters.add(Counter(alias=owner_uname), owner=owner)

    def join(self, alias: str, username: str, uow: AbstractUnitOfWork) -> bool:
        with uow:
            if not (user:=uow.users.get(username)):
                raise NonExisting(f"User {username} does not exists")
            
            if not (counter:=uow.counters.get(alias)):
                raise NonExisting(f"Counter {alias} does not exists")

            return counter.join(user)

    def update(self, alias: str, username: str, uow: AbstractUnitOfWork) -> Counter:
        with uow:
            if not (user:=uow.users.get(username)):
                raise NonExisting(f"User {username} does not exists")
            
            if not (counter:=uow.counters.get(alias)):
                raise NonExisting(f"Counter {alias} does not exists")

            counter.update_member(user)

            return counter