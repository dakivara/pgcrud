from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal

from psycopg.sql import SQL, Composed, Identifier


__all__ = [
    'SortOperator',
    'Ascending',
    'Descending',
]


@dataclass
class SortOperator:
    name: str

    @abstractmethod
    def get_composed(self) -> Composed | None:
        pass


class Ascending(SortOperator):

    def get_composed(self) -> Composed:
        return SQL('{} ASC').format(Identifier(self.name))


class Descending(SortOperator):

    def get_composed(self) -> Composed:
        return SQL('{} DESC').format(Identifier(self.name))


@dataclass
class Direction(SortOperator):
    value: bool | Literal[0, 1] | None

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL('{} {}').format(Identifier(self.name), SQL('ASC') if self.value else SQL('DESC'))
