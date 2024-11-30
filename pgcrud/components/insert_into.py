from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.values import Values
from pgcrud.types import InsertIntoValueType, ValuesValueItemType


if TYPE_CHECKING:
    from pgcrud.expr import ReferenceExpr


__all__ = ['InsertInto']


@dataclass
class InsertInto(Component):
    value: InsertIntoValueType

    def get_single_composed(self) -> Composed:
        return SQL('INSERT INTO {}').format(self.value.get_composed())

    def get_exprs(self) -> tuple['ReferenceExpr', ...]:
        return self.value.children

    def VALUES(self, *args: ValuesValueItemType, **kwargs: Any) -> Values:
        return Values(self.components, args, kwargs)
