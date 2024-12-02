from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.operators import FilterOperator
from pgcrud.operators.operator import Operator


if TYPE_CHECKING:
    from pgcrud.expr import Expr


__all__ = [
    'JoinOperator',
    'Join',
    'InnerJoin',
    'FullJoin',
    'LeftJoin',
    'RightJoin',
    'CrossJoin',
]


@dataclass(repr=False)
class JoinOperator(Operator):

    def __bool__(self) -> bool:
        return True

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


@dataclass(repr=False)
class Join(JoinOperator):
    expr: 'Expr'
    on: 'FilterOperator'

    @abstractmethod
    def get_composed(self) -> Composed:
        return SQL('JOIN {} ON {}').format(self.expr.get_composed(), self.on.get_composed())


@dataclass(repr=False)
class InnerJoin(JoinOperator):
    expr: 'Expr'
    on: 'FilterOperator'

    @abstractmethod
    def get_composed(self) -> Composed:
        return SQL('INNER JOIN {} ON {}').format(self.expr.get_composed(), self.on.get_composed())


@dataclass(repr=False)
class FullJoin(JoinOperator):
    expr: 'Expr'
    on: 'FilterOperator'

    @abstractmethod
    def get_composed(self) -> Composed:
        return SQL('FULL JOIN {} ON {}').format(self.expr.get_composed(), self.on.get_composed())


@dataclass(repr=False)
class LeftJoin(JoinOperator):
    expr: 'Expr'
    on: 'FilterOperator'

    @abstractmethod
    def get_composed(self) -> Composed:
        return SQL('LEFT JOIN {} ON {}').format(self.expr.get_composed(), self.on.get_composed())


@dataclass(repr=False)
class RightJoin(JoinOperator):
    expr: 'Expr'
    on: 'FilterOperator'

    @abstractmethod
    def get_composed(self) -> Composed:
        return SQL('RIGHT JOIN {} ON {}').format(self.expr.get_composed(), self.on.get_composed())


@dataclass(repr=False)
class CrossJoin(JoinOperator):
    expr: 'Expr'

    @abstractmethod
    def get_composed(self) -> Composed:
        return SQL('CROSS JOIN {}').format(self.expr.get_composed())
