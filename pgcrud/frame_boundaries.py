from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from psycopg.sql import SQL, Composed


__all__ = [
    'FrameBoundary',
    'UnboundedPreceding',
    'UnboundedFollowing',
    'CurrentRow',
    'UNBOUNDED_PRECEDING',
    'UNBOUNDED_FOLLOWING',
    'CURRENT_ROW',
    'PRECEDING',
    'FOLLOWING',
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
    value: Any

    def get_composed(self) -> Composed:
        return SQL('{} PRECEDING').format(self.value)


class UnboundedFollowing(FrameBoundary):

    def get_composed(self) -> Composed:
        return Composed([SQL('UNBOUNDED FOLLOWING')])


@dataclass(repr=False)
class Following(FrameBoundary):
    value: Any

    def get_composed(self) -> Composed:
        return SQL('{} FOLLOWING').format(self.value)


class CurrentRow(FrameBoundary):

    def get_composed(self) -> Composed:
        return Composed([SQL('CURRENT ROW')])


UNBOUNDED_PRECEDING = UnboundedPreceding()
UNBOUNDED_FOLLOWING = UnboundedFollowing()
CURRENT_ROW = CurrentRow()


def PRECEDING(value: Any) -> Preceding:
    return Preceding(value)


def FOLLOWING(value: Any) -> Following:
    return Following(value)
