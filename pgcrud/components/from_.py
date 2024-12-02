from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.group_by import GroupBy
from pgcrud.components.having import Having
from pgcrud.components.limit import Limit
from pgcrud.components.offset import Offset
from pgcrud.components.order_by import OrderBy
from pgcrud.components.where import Where
from pgcrud.types import FromValueType, GroupByValueType, HavingValueType, WhereValueType, OrderByValueType


__all__ = ['From']


@dataclass(repr=False)
class From(Component):
    value: FromValueType

    def get_single_composed(self) -> Composed:
        return SQL('FROM {}').format(self.value.get_composed())

    def WHERE(self, value: WhereValueType) -> Where:
        return Where(self.components, value)

    def GROUP_BY(self, value: GroupByValueType) -> GroupBy:
        return GroupBy(self.components, value)

    def HAVING(self, value: HavingValueType) -> Having:
        return Having(self.components, value)

    def ORDER_BY(self, value: OrderByValueType) -> OrderBy:
        return OrderBy(self.components, value)

    def LIMIT(self, value: int | None = None) -> Limit:
        return Limit(self.components, value)

    def OFFSET(self, value: int | None = None) -> Offset:
        return Offset(self.components, value)
