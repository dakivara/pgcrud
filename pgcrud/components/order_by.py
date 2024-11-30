from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.limit import Limit
from pgcrud.components.offset import Offset
from pgcrud.types import OrderByValueType
from pgcrud.utils import ensure_list


__all__ = ['OrderBy']


@dataclass(repr=False)
class OrderBy(Component):
    value: OrderByValueType

    def get_single_composed(self) -> Composed:

        composed_list = []

        for v in ensure_list(self.value):
            if v:
                composed_list.append(v.get_composed())

        if composed_list:
            return SQL('ORDER BY {}').format(SQL(', ').join(composed_list))
        else:
            return Composed([])

    def LIMIT(self, value: int | None = None) -> Limit:
        return Limit(self.components, value)

    def OFFSET(self, value: int | None = None) -> Offset:
        return Offset(self.components, value)
