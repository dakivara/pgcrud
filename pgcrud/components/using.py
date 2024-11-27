from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.returning import Returning
from pgcrud.components.where import Where
from pgcrud.types import ReturningValueType, UsingValueType, WhereValueType


__all__ = ['Using']


@dataclass(repr=False)
class Using(Component):
    value: UsingValueType

    def get_single_composed(self) -> Composed:
        return SQL('USING {}').format(self.value.get_composed())

    def where(self, value: WhereValueType) -> Where:
        return Where(self.components, value)

    def returning(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
