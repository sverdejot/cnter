from .abstract import AbstractRepository
from cnter.core.domain.model import Counter

class SQLCounterRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session
        super().__init__()

    def add(self, counter: Counter):
        self.seen.add(counter)
        return self._add(counter)

    def get(self, alias: str):
        if counter := self._get(alias):
            self.seen.add(counter)
        return counter

    def _add(self, counter: Counter):
        return self.session.add(counter)

    def _get(self, alias: str):
        return self.session.query(Counter).filter_by(alias=alias).one()