from ...domain.repositories import CounterRepository

from ...domain.entities import Counter

from ...domain.value_objects import CounterId

class CounterFinder:
    repo: CounterRepository

    def __init__(self, repo: CounterRepository):
        self.repo = repo

    def __call__(self, counterId: CounterId) -> Counter:
        return self.repo.find(counterId)