from .abstract import AbstractRepository
from cnter.core.domain.model import User

class SQLUserRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
        super().__init__()

    def add(self, user: User):
        self.seen.add(user)
        return self._add(user)
    
    def get(self, username: str):
        if user := self._get(username):
            self.seen.add(user)
        return user

    def _add(self, user: User):
        return self.session.add(user)

    def _get(self, username: str):
        return self.session.query(User).filter_by(username=username).one()