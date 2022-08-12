from dataclasses import dataclass

class DomainEvent:
    pass

@dataclass
class UserNotFound(DomainEvent):
    username: str

@dataclass
class CounterNotFound(DomainEvent):
    alias: str

@dataclass
class CounterAlreadyExists(DomainEvent):
    alias: str

@dataclass
class ExceededMaximumState(DomainEvent):
    max_state: int

@dataclass
class ExceededMaximumMembers(DomainEvent):
    max_users: int