from dataclasses import dataclass
from typing import Any

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.values import Values
from pgcrud.types import InsertIntoValueType, ValuesValueItemType


__all__ = ['InsertInto']


@dataclass
class InsertInto(Component):
    value: InsertIntoValueType

    def get_single_composed(self) -> Composed:
        return SQL('INSERT INTO {}').format(self.value.get_composed())

    def get_positional_placeholder(self) -> SQL:
        return SQL(Composed([SQL('('), SQL(', ').join([SQL('{}')] * len(self.value.cols)), SQL(')')]).as_string())    # type: ignore

    def get_named_placeholder(self) -> SQL:
        return SQL(Composed([SQL('('), SQL(', ').join([SQL(f'{{{col.name}}}') for col in self.value.cols]), SQL(')')]).as_string())  # type: ignore

    def values(self, *args: ValuesValueItemType, **kwargs: Any) -> Values:
        return Values(self.components, args, kwargs)
