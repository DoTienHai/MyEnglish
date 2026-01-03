# shared/observer.py
from typing import Callable, Generic, TypeVar

T = TypeVar("T")

class ObserverBase(Generic[T]):
    def __init__(self, value: T):
        self.value = value
        self._subs: list[Callable[[T], None]] = []

    def subscribe(self, callback: Callable[[T], None]):
        self._subs.append(callback)

    def notify(self, value: T):
        self.value = value
        for cb in self._subs:
            cb(value)

