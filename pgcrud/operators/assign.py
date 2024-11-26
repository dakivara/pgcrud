from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.operators.operator import Operator

if TYPE_CHECKING:
    from pgcrud.col import Col


__all__ = [
    'Assign',
]


@dataclass(repr=False)
class Assign(Operator):
    left: 'Col'
    right: 'Col'

    def get_composed(self) -> Composed:
        if self.left and self.right:
            return SQL("{} = {}").format(self.left.get_composed(), self.right.get_composed())
        else:
            return Composed([])
