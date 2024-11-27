from abc import abstractmethod
from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.group_by import GroupBy
from pgcrud.components.having import Having
from pgcrud.components.limit import Limit
from pgcrud.components.offset import Offset
from pgcrud.components.order_by import OrderBy
from pgcrud.components.where import Where
from pgcrud.operators import JoinOn
from pgcrud.types import GroupByValueType, HavingValueType, JoinValueType, OrderByValueType, WhereValueType
from pgcrud.utils import ensure_list


__all__ = [
    'JoinComponent',
    'Join',
    'InnerJoin',
    'LeftJoin',
    'RightJoin',
    'FullJoin',
    'CrossJoin',
]


@dataclass(repr=False)
class JoinComponent(Component):
    value: JoinValueType

    @abstractmethod
    def get_composed_join_type(self, on: JoinOn) -> Composed:
        pass

    def get_single_composed(self) -> Composed:

        composed_list = []

        for v in ensure_list(self.value):
            if v:
                composed_list.append(SQL('{} {}').format(self.get_composed_join_type(v), v.get_composed()))

        if composed_list:
            return SQL(' ').join(composed_list)
        else:
            return Composed([])

    def join(self, value: JoinValueType) -> 'Join':
        return Join(self.components, value)

    def inner_join(self, value: JoinValueType) -> 'InnerJoin':
        return InnerJoin(self.components, value)

    def left_join(self, value: JoinValueType) -> 'LeftJoin':
        return LeftJoin(self.components, value)

    def where(self, value: WhereValueType) -> Where:
        return Where(self.components, value)

    def group_by(self, value: GroupByValueType) -> GroupBy:
        return GroupBy(self.components, value)

    def having(self, value: HavingValueType) -> Having:
        return Having(self.components, value)

    def order_by(self, value: OrderByValueType) -> OrderBy:
        return OrderBy(self.components, value)

    def limit(self, value: int | None = None) -> Limit:
        return Limit(self.components, value)

    def offset(self, value: int | None = None) -> Offset:
        return Offset(self.components, value)


@dataclass(repr=False)
class Join(JoinComponent):

    def get_composed_join_type(self, on: JoinOn) -> Composed:
        return on.get_composed_join_type()


@dataclass(repr=False)
class InnerJoin(JoinComponent):

    def get_composed_join_type(self, on: JoinOn) -> Composed:
        return Composed([SQL('INNER JOIN')])


@dataclass(repr=False)
class LeftJoin(JoinComponent):

    def get_composed_join_type(self, on: JoinOn) -> Composed:
        return Composed([SQL('LEFT JOIN')])


@dataclass(repr=False)
class RightJoin(JoinComponent):

    def get_composed_join_type(self, on: JoinOn) -> Composed:
        return Composed([SQL('RIGHT JOIN')])


@dataclass(repr=False)
class FullJoin(JoinComponent):

    def get_composed_join_type(self, on: JoinOn) -> Composed:
        return Composed([SQL('FULL JOIN')])


@dataclass(repr=False)
class CrossJoin(JoinComponent):

    def get_composed_join_type(self, on: JoinOn) -> Composed:
        return Composed([SQL('CROSS JOIN')])
