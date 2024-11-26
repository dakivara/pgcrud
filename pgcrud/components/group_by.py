from dataclasses import dataclass

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.types import GroupByValueType
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
