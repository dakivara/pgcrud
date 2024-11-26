from dataclasses import dataclass

from psycopg.sql import SQL, Composed, Literal

from pgcrud.components import Component


__all__ = ['Offset']


@dataclass(repr=False)
class Offset(Component):
    value: int | None = None

    def get_single_composed(self) -> Composed:
        if self.value:
            return SQL('OFFSET {}').format(Literal(self.value))
        else:
            return Composed([])
