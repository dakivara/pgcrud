from dataclasses import dataclass

from psycopg.sql import SQL, Composed, Identifier

from pgcrud._c import c
from pgcrud._col import SingleCol


__all__ = [
    'Tab',
]


@dataclass
class Tab:
    _pgcrud_name: str

    def get_composed(self) -> Composed:
        return SQL('{}').format(Identifier(self._pgcrud_name))

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, item) -> SingleCol:
        return SingleCol(item, self._pgcrud_name)
