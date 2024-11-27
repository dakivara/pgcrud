from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components import Component, OrderBy, Limit, Offset
from pgcrud.types import HavingValueType, OrderByValueType


__all__ = ['Having']


@dataclass(repr=False)
class Having(Component):
    value: HavingValueType

    def get_single_composed(self) -> Composed:
        return SQL('HAVING {}').format(self.get_composed())

    def order_by(self, value: OrderByValueType) -> OrderBy:
        return OrderBy(self.components, value)

    def limit(self, value: int) -> Limit:
        return Limit(self.components, value)

    def offset(self, value: int) -> Offset:
        return Offset(self.components, value)
