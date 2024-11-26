from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.types import UpdateValueType


__all__ = ['Update']


@dataclass(repr=False)
class Update(Component):
    value: UpdateValueType

    def get_single_composed(self) -> Composed:
        return SQL('UPDATE {}').format(self.value.get_composed())
