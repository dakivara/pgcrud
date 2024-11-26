from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.group_by import GroupBy
from pgcrud.components.limit import Limit
from pgcrud.components.offset import Offset
from pgcrud.components.order_by import OrderBy
from pgcrud.components.returning import Returning
from pgcrud.types import GroupByValueType, ReturningValueType, WhereValueType, OrderByValueType


__all__ = ['Where']


@dataclass(repr=False)
class Where(Component):
    value: WhereValueType

    def get_single_composed(self) -> Composed:
        if self.value:
            return SQL('WHERE {}').format(self.value.get_composed())
        else:
            return Composed([])

    def group_by(self, value: GroupByValueType) -> GroupBy:
        return GroupBy(self.components, value)

    def order_by(self, value: OrderByValueType) -> OrderBy:
        return OrderBy(self.components, value)

    def limit(self, value: int) -> Limit:
        return Limit(self.components, value)

    def offset(self, value: int) -> Offset:
        return Offset(self.components, value)

    def returning(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
