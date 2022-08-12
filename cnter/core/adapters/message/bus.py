from cnter.core.domain.events import(
    DomainEvent,
    UserNotFound,
    CounterAlreadyExists,
    CounterNotFound
)

from typing import TypedDict

import abc

class AbstractMessageBus(abc.ABC):
    @abc.abstractmethod
    def handle(self):
        raise NotImplementedError

def handle(event: DomainEvent, *args, **kwargs):
    for handler in HANDLERS(event):
        return handler(event, *args, **kwargs)

def handle_not_found(event, *args, **kwargs):
    print(f"Resource {event} not found")

HANDLERS = {
    UserNotFound: handle_not_found,
    CounterAlreadyExists: handle_not_found,
    CounterNotFound: handle_not_found,
}