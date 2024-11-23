from dataclasses import dataclass

from psycopg.sql import SQL, Composed, Identifier

from pgcrud._c import c
from pgcrud._col import SingleCol


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
