from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable

from psycopg.sql import SQL, Composed


__all__ = [
    'FrameBoundary',
    'UnboundedPreceding',
    'UnboundedFollowing',
    'CurrentRow',
    'UNBOUNDED_PRECEDING',
    'PRECEDING',
    'UNBOUNDED_FOLLOWING',
    'FOLLOWING',
    'CURRENT_ROW',
]


class FrameBoundary:

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return str(self)

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


class UnboundedPreceding(FrameBoundary):

    def get_composed(self) -> Composed:
        return Composed([SQL('UNBOUNDED PRECEEDING')])


@dataclass(repr=False)
class Preceding(FrameBoundary):
    value: int

    def get_composed(self) -> Composed:
        return SQL('{} PRECEDING').format(self.value)


class UnboundedFollowing(FrameBoundary):

    def get_composed(self) -> Composed:
        return Composed([SQL('UNBOUNDED FOLLOWING')])


@dataclass(repr=False)
class Following(FrameBoundary):
    value: int

    def get_composed(self) -> Composed:
        return SQL('{} FOLLOWING').format(self.value)


class CurrentRow(FrameBoundary):

    def get_composed(self) -> Composed:
        return Composed([SQL('CURRENT ROW')])


UNBOUNDED_PRECEDING = UnboundedPreceding()
PRECEDING: Callable[[int], Preceding] = lambda x: Preceding(x)
UNBOUNDED_FOLLOWING = UnboundedFollowing()
FOLLOWING: Callable[[int], Following] = lambda x: Following(x)
CURRENT_ROW = CurrentRow()
