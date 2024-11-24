from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed, Identifier

from pgcrud.c import c
from pgcrud.col import ToJsonCol
from pgcrud.operators.join_operators import Join, InnerJoin


if TYPE_CHECKING:
    from pgcrud.operators.filter_operators import FilterOperator


__all__ = [
    'Tab',
    'SimpleTab',
    'AliasTab',
]


@dataclass
class Tab:

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    @property
    @abstractmethod
    def c(self) -> type[c]:
        pass

    def as_(self, alias) -> 'AliasTab':
        return AliasTab(self, alias)

    def join(self, on: 'FilterOperator') -> Join:
        return Join(self, on)

    def inner_join(self, on: 'FilterOperator') -> InnerJoin:
        return InnerJoin(self, on)

    def to_json(self) -> ToJsonCol:
        return ToJsonCol(self)


@dataclass(repr=False)
class SimpleTab(Tab):
    name: str

    def get_composed(self) -> Composed:
        return SQL('{}').format(Identifier(self.name))

    @property
    def c(self) -> type[c]:
        return c[self]


@dataclass(repr=False)
class AliasTab(Tab):
    tab: Tab
    alias: str

    def get_composed(self) -> Composed:
        return SQL('{} AS {}').format(self.tab.get_composed(), Identifier(self.alias))

    @property
    def c(self) -> type[c]:
        return c[self.tab]
