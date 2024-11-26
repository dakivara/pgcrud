from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.group_by import GroupBy
from pgcrud.components.join import Join, InnerJoin, LeftJoin
from pgcrud.components.limit import Limit
from pgcrud.components.offset import Offset
from pgcrud.components.order_by import OrderBy
from pgcrud.components.where import Where
from pgcrud.types import FromValueType, GroupByValueType, JoinValueType, WhereValueType, OrderByValueType


__all__ = ['From']


@dataclass(repr=False)
class From(Component):
    value: FromValueType

    def get_single_composed(self) -> Composed:
        return SQL('FROM {}').format(self.value.get_composed())

    def where(self, value: WhereValueType) -> Where:
        return Where(self.components, value)

    def group_by(self, value: GroupByValueType) -> GroupBy:
        return GroupBy(self.components, value)

    def order_by(self, value: OrderByValueType) -> OrderBy:
        return OrderBy(self.components, value)

    def limit(self, value: int | None = None) -> Limit:
        return Limit(self.components, value)

    def offset(self, value: int | None = None) -> Offset:
        return Offset(self.components, value)

    def join(self, value: JoinValueType) -> Join:
        return Join(self.components, value)

    def inner_join(self, value: JoinValueType) -> InnerJoin:
        return InnerJoin(self.components, value)

    def left_join(self, value: JoinValueType) -> LeftJoin:
        return LeftJoin(self.components, value)
