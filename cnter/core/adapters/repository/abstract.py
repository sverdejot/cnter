import abc

from cnter.core.domain.model import BaseModel

class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError