from uuid import UUID
from abc import ABCMeta

from dataclasses import dataclass

@dataclass(frozen=True)
class Property(metaclass=ABCMeta):
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

@dataclass(frozen=True)
class UuidProperty(Property, metaclass=ABCMeta):
    value: UUID
    
    def __str__(self):
        return str(self.value)

@dataclass(frozen=True)
class IntegerProperty(Property, metaclass=ABCMeta):
    value: int

@dataclass(frozen=True)
class BooleanProperty(Property, metaclass=ABCMeta):
    value: bool