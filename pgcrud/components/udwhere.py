from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.returning import Returning
from pgcrud.types import ReturningValueType, WhereValueType


__all__ = ['UDWhere']


@dataclass(repr=False)
class UDWhere(Component):
    value: WhereValueType

    def get_single_composed(self) -> Composed:
        return SQL('WHERE {}').format(self.value.get_composed())

    def returning(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
