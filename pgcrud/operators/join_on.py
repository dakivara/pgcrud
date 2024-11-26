from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.operators.operator import Operator
from pgcrud.types import HowValueType

if TYPE_CHECKING:
    from pgcrud.operators.filter import FilterOperator
    from pgcrud.tab import Tab


__all__ = ['JoinOn']


@dataclass(repr=False)
class JoinOn(Operator):
    tab: 'Tab'
    operator: 'FilterOperator'
    how: HowValueType | None = None

    def get_composed_join_type(self) -> Composed:
        if self.how:
            return SQL('{} JOIN').format(SQL(self.how))
        else:
            return Composed([SQL('JOIN')])

    def get_composed(self) -> Composed:
        if self.operator:
            return SQL('{} ON {}').format(self.tab.get_composed(), self.operator.get_composed())
        else:
            return Composed([])
