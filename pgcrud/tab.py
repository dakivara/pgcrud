from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed, Identifier

from pgcrud.col_generator import ColGenerator as c
from pgcrud.operators import JoinOn
from pgcrud.types import HowValueType


if TYPE_CHECKING:
    from pgcrud.col import SingleCol
    from pgcrud.operators import FilterOperator


__all__ = [
    'Tab',
    'SimpleTab',
    'AliasTab',
]


@dataclass
class Tab:

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    @property
    @abstractmethod
    def c(self) -> type[c]:
        pass

    def as_(self, alias) -> 'AliasTab':
        return AliasTab(self, alias)

    def on(self, operator: 'FilterOperator', how: HowValueType | None = None) -> JoinOn:
        return JoinOn(self, operator, how)


@dataclass(repr=False)
class SimpleTab(Tab):
    name: str
    cols: tuple['SingleCol', ...] = ()

    def __getitem__(self, cols: 'SingleCol | tuple[SingleCol, ...]') -> 'SimpleTab':
        if not isinstance(cols, tuple):
            cols = (cols,)
        return SimpleTab(self.name, cols)

    def get_composed(self) -> Composed:
        if self.cols:
            return SQL('{} ({})').format(Identifier(self.name), SQL(', ').join([col.get_composed() for col in self.cols]))
        else:
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
