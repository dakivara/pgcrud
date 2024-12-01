from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.returning import Returning
from pgcrud.components.udwhere import UDWhere
from pgcrud.components.using import Using
from pgcrud.types import DeleteFromValueType, ReturningValueType, UsingValueType, WhereValueType


__all__ = ['DeleteFrom']


@dataclass(repr=False)
class DeleteFrom(Component):
    value: DeleteFromValueType

    def get_single_composed(self) -> Composed:
        return SQL('DELETE FROM {}').format(self.value.get_composed())

    def USING(self, value: UsingValueType) -> Using:
        return Using(self.components, value)

    def WHERE(self, value: WhereValueType) -> UDWhere:
        return UDWhere(self.components, value)

    def RETURNING(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
