from dataclasses import dataclass


@dataclass(frozen=True)
class CounterStatus:
    value: int

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)
        