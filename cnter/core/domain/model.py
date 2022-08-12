from dataclasses import dataclass
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.events = []

class User(BaseModel):
    def __init__(self, username: str):
        super().__init__()
        self.username = username

    def __hash__(self):
        return hash(self.username)

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.username == other.username

@dataclass(unsafe_hash=True)
class Update:
    member: User
    ts: float

class Counter(BaseModel):
    def __init__(self, owner: User, alias: str):
        super().__init__()
        self.alias = alias
        self.owner = owner
        self.updates = set()
        self.members = set()
    
    @property
    def state(self):
        return len(self.updates)

    def member_update(self, member: User):
        if member in self.members:
            self.updates.add(Update(member=member, ts=datetime.now().timestamp()))

    def join(self, user: User) -> bool:
        if user in self.members or user == self.owner:
            return False
        self.members.add(user)
        return True