from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.operators.operator import Operator
from pgcrud.undefined import Undefined


if TYPE_CHECKING:
    from pgcrud.expr import Expr


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
    expr: 'Expr'
    flag: bool | type[Undefined] = True

    def get_composed(self) -> Composed:
        if not self.expr or self.flag is Undefined:
            return Composed([])
        elif self.flag:
            return SQL("{} ASC").format(self.expr.get_composed())
        else:
            return SQL("{} DESC").format(self.expr.get_composed())


@dataclass(repr=False)
class Descending(SortOperator):
    expr: 'Expr'
    flag: bool | type[Undefined] = True

    def get_composed(self) -> Composed:
        if not self.expr or self.flag is Undefined:
            return Composed([])
        elif self.flag:
            return SQL("{} DESC").format(self.expr.get_composed())
        else:
            return SQL("{} ASC").format(self.expr.get_composed())
