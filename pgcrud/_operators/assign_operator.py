from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

if TYPE_CHECKING:
    from pgcrud._col import Col


__all__ = [
    'Assign',
]


@dataclass
class Assign:
    left: 'Col'
    right: 'Col'

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return len(self.get_composed()._obj) > 0

    def get_composed(self) -> Composed:
        if self.left.is_undefined_col or self.right.is_undefined_col:
            return Composed([])
        else:
            return SQL("{} = {}").format(self.left.get_composed(), self.right.get_composed())
