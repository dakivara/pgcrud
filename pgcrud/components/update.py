from dataclasses import dataclass
from typing import Any

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.set_ import Set
from pgcrud.types import SetColsType, SetValueType, UpdateValueType


__all__ = ['Update']


@dataclass(repr=False)
class Update(Component):
    value: UpdateValueType

    def get_single_composed(self) -> Composed:
        return SQL('UPDATE {}').format(self.value.get_composed())

    def SET(self, cols: SetColsType, value: SetValueType, **kwargs: Any) -> Set:
        return Set(self.components, cols, value, kwargs)
