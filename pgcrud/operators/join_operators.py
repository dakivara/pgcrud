from abc import abstractmethod
from typing import TYPE_CHECKING

from dataclasses import dataclass

from psycopg.sql import SQL, Composed

if TYPE_CHECKING:
    from pgcrud.tab import Tab
    from pgcrud.operators.filter_operators import FilterOperator


__all__ = [
    'JoinOperator',
    'Join',
    'InnerJoin',
]


@dataclass
class JoinOperator:
    tab: 'Tab'
    filter_operator: 'FilterOperator'

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return len(self.get_composed()._obj) > 0

    @property
    @abstractmethod
    def operator(self) -> SQL:
        pass

    def get_composed(self) -> Composed:
        return SQL('{} {} ON {}').format(self.operator, self.tab.get_composed(), self.filter_operator.get_composed())


@dataclass(repr=False)
class Join(JoinOperator):

    @property
    def operator(self) -> SQL:
        return SQL('JOIN')


@dataclass(repr=False)
class InnerJoin(JoinOperator):

    @property
    def operator(self) -> SQL:
        return SQL('INNER JOIN')
