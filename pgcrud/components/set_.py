from collections.abc import Sequence
from dataclasses import dataclass

from psycopg.sql import SQL, Composed


from pgcrud.components.component import Component
from pgcrud.components.returning import Returning
from pgcrud.components.ufrom import UFrom
from pgcrud.components.udwhere import UDWhere
from pgcrud.types import FromValueType, ReturningValueType, SetColsType, SetValueType, AdditionalValuesType, WhereValueType


__all__ = ['Set']


@dataclass(repr=False)
class Set(Component):
    cols: SetColsType
    value: SetValueType
    additional_values: AdditionalValuesType

    def get_single_composed(self) -> Composed:

        composed_cols = []
        composed_values = []

        if isinstance(self.value, Sequence):
            for col, v in zip(self.cols, self.value, strict=True):
                composed_cols.append(col.get_composed())
                composed_values.append(v)

        elif isinstance(self.value, dict):
            params = self.additional_values.copy()
            params.update(self.value)

            for col in self.cols:
                composed_cols.append(col.get_composed())
                composed_values.append(params[col.name])

        else:
            params = self.additional_values.copy()
            params.update(self.value.model_dump(by_alias=True))

            for col in self.cols:
                composed_cols.append(col.get_composed())
                composed_values.append(params[col.name])

        if len(composed_cols) > 1:
            return SQL('SET ({}) = ({})').format(SQL(', ').join(composed_cols), SQL(', ').join(composed_values))
        elif len(composed_cols) == 1:
            return SQL('SET {} = {}').format(composed_cols[0], composed_values[0])
        else:
            return Composed([])

    def from_(self, value: FromValueType) -> UFrom:
        return UFrom(self.components, value)

    def where(self, value: WhereValueType) -> UDWhere:
        return UDWhere(self.components, value)

    def returning(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
