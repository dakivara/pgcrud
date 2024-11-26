from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.limit import Limit
from pgcrud.components.offset import Offset
from pgcrud.components.order_by import OrderBy
from pgcrud.types import GroupByValueType, OrderByValueType
from pgcrud.utils import ensure_list


__all__ = ['GroupBy']


@dataclass(repr=False)
class GroupBy(Component):
    value: GroupByValueType

    def get_single_composed(self) -> Composed:
        composed_list = [col.get_composed() for col in ensure_list(self.value) if col]

        if composed_list:
            return SQL('GROUP BY {}').format(SQL(', ').join(composed_list))
        else:
            return Composed([])

    def order_by(self, value: OrderByValueType) -> OrderBy:
        return OrderBy(self.components, value)

    def limit(self, value: int) -> Limit:
        return Limit(self.components, value)

    def offset(self, value: int) -> Offset:
        return Offset(self.components, value)
