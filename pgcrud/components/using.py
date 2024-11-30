from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.returning import Returning
from pgcrud.components.udwhere import UDWhere
from pgcrud.types import ReturningValueType, UsingValueType, WhereValueType


__all__ = ['Using']


@dataclass(repr=False)
class Using(Component):
    value: UsingValueType

    def get_single_composed(self) -> Composed:
        return SQL('USING {}').format(self.value.get_composed())

    def WHERE(self, value: WhereValueType) -> UDWhere:
        return UDWhere(self.components, value)

    def RETURNING(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
