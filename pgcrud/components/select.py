from dataclasses import dataclass

from psycopg.sql import SQL, Composed
from pydantic import BaseModel

from pgcrud.col import Col, SingleCol
from pgcrud.components import Component
from pgcrud.components.from_ import From
from pgcrud.types import SelectValueType, FromValueType
from pgcrud.utils import ensure_list


__all__ = ['Select']


@dataclass(repr=False)
class Select(Component):
    value: SelectValueType

    def get_single_composed(self) -> Composed:

        composed_list = []

        if isinstance(self.value, type) and issubclass(self.value, BaseModel):
            for name, field in self.value.model_fields.items():
                col = SingleCol(name)

                for m in field.metadata:
                    if isinstance(m, Col):
                        col = m
                        break

                composed_list.append(col.get_composed())

        else:
            for v in ensure_list(self.value):
                if v:
                    composed_list.append(v.get_composed())

        if composed_list:
            return SQL('SELECT {}').format(SQL(', ').join(composed_list))
        else:
            return Composed([])

    def from_(self, value: FromValueType) -> From:
        return From(self.components, value)
