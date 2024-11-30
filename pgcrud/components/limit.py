from dataclasses import dataclass

from psycopg.sql import SQL, Composed, Literal

from pgcrud.components import Component
from pgcrud.components.offset import Offset


__all__ = ['Limit']


@dataclass(repr=False)
class Limit(Component):
    value: int | None = None

    def get_single_composed(self) -> Composed:
        if self.value:
            return SQL('LIMIT {}').format(Literal(self.value))
        else:
            return Composed([])

    def OFFSET(self, value: int | None = None) -> Offset:
        return Offset(self.components, value)
