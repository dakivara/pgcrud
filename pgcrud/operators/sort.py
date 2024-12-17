from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.operators.operator import Operator


if TYPE_CHECKING:
    from pgcrud.expr import Expr


__all__ = [
    'SortOperator',
    'UndefinedSort',
    'Ascending',
    'Descending',
]


@dataclass(repr=False)
class SortOperator(Operator):

    def __bool__(self) -> bool:
        return not isinstance(self, UndefinedSort)

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


@dataclass(repr=False)
class UndefinedSort(SortOperator):

    def get_composed(self) -> Composed:
        return Composed([])


@dataclass(repr=False)
class Ascending(SortOperator):
    expr: 'Expr'
    flag: bool = True

    def get_composed(self) -> Composed:
        if self.flag:
            return SQL("{} ASC").format(self.expr.get_composed())
        else:
            return SQL("{} DESC").format(self.expr.get_composed())


@dataclass(repr=False)
class Descending(SortOperator):
    expr: 'Expr'
    flag: bool = True

    def get_composed(self) -> Composed:
        if self.flag:
            return SQL("{} DESC").format(self.expr.get_composed())
        else:
            return SQL("{} ASC").format(self.expr.get_composed())
