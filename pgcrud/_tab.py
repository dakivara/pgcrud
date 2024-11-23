from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed, Identifier

from pgcrud._c import c
from pgcrud._operators.join_operators import Join, InnerJoin


if TYPE_CHECKING:
    from pgcrud._operators.filter_operators import FilterOperator


__all__ = [
    'Tab',
]


@dataclass
class Tab:
    name: str

    def get_composed(self) -> Composed:
        return SQL('{}').format(Identifier(self.name))

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    @property
    def c(self) -> type[c]:
        return c[self]

    def join(self, on: 'FilterOperator') -> Join:
        return Join(self, on)

    def inner_join(self, on: 'FilterOperator') -> InnerJoin:
        return InnerJoin(self, on)
