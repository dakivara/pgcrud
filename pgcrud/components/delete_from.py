from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.where import Where
from pgcrud.components.returning import Returning
from pgcrud.types import DeleteFromValueType, ReturningValueType, WhereValueType


__all__ = ['DeleteFrom']


@dataclass(repr=False)
class DeleteFrom(Component):
    value: DeleteFromValueType

    def get_single_composed(self) -> Composed:
        return SQL('DELETE FROM {}').format(self.value.get_composed())

    def where(self, value: WhereValueType) -> Where:
        return Where(self.components, value)

    def returning(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
