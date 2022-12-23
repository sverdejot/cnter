from uuid import UUID
from abc import ABC

class UuidProperty(ABC):
    value: UUID

    def value(self):
        return self.value

class IntegerProperty(ABC):
    value: int

    def value(self):
        return self.value

class BooleanProperty(ABC):
    value: bool

    def value(self):
        return self.value