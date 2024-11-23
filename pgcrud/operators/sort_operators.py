from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.undefined import Undefined


if TYPE_CHECKING:
    from pgcrud.col import Col


__all__ = [
    'SortOperator',
    'Ascending',
    'Descending',
    'CompositeSort'
]


@dataclass
class SortOperator:

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return len(self.get_composed()._obj) > 0

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


@dataclass(repr=False)
class Ascending(SortOperator):
    col: 'Col'
    flag: bool = True

    def get_composed(self) -> Composed:
        if self.col.is_undefined_col or self.flag is Undefined:
            return Composed([])
        elif self.flag:
            return SQL("{} ASC").format(self.col.get_composed())
        else:
            return SQL("{} DESC").format(self.col.get_composed())


@dataclass(repr=False)
class Descending(SortOperator):
    col: 'Col'
    flag: bool = True

    def get_composed(self) -> Composed:
        if self.col.is_undefined_col or self.flag is Undefined:
            return Composed([])
        elif self.flag:
            return SQL("{} DESC").format(self.col.get_composed())
        else:
            return SQL("{} ASC").format(self.col.get_composed())


@dataclass(repr=False)
class CompositeSort(SortOperator):
    operators: list[SortOperator]

    def get_composed(self) -> Composed:
        return SQL(', ').join([operator.get_composed() for operator in self.operators if operator])
