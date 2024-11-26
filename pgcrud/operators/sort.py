from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.operators.operator import Operator
from pgcrud.undefined import Undefined


if TYPE_CHECKING:
    from pgcrud.col import Col


__all__ = [
    'SortOperator',
    'Ascending',
    'Descending',
]


@dataclass(repr=False)
class SortOperator(Operator):

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


@dataclass(repr=False)
class Ascending(SortOperator):
    col: 'Col'
    flag: bool | type[Undefined] = True

    def get_composed(self) -> Composed:
        if not self.col or self.flag is Undefined:
            return Composed([])
        elif self.flag:
            return SQL("{} ASC").format(self.col.get_composed())
        else:
            return SQL("{} DESC").format(self.col.get_composed())


@dataclass(repr=False)
class Descending(SortOperator):
    col: 'Col'
    flag: bool | type[Undefined] = True

    def get_composed(self) -> Composed:
        if not self.col or self.flag is Undefined:
            return Composed([])
        elif self.flag:
            return SQL("{} DESC").format(self.col.get_composed())
        else:
            return SQL("{} ASC").format(self.col.get_composed())
