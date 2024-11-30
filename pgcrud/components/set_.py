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

        composed_exprs = []
        composed_values = []

        if isinstance(self.value, Sequence):
            for expr, v in zip(self.cols, self.value, strict=True):
                composed_exprs.append(expr.get_composed())
                composed_values.append(v)

        elif isinstance(self.value, dict):
            params = self.additional_values.copy()
            params.update(self.value)

            for expr in self.cols:
                composed_exprs.append(expr.get_composed())
                composed_values.append(params[expr._name])

        else:
            params = self.additional_values.copy()
            params.update(self.value.model_dump(by_alias=True))

            for expr in self.cols:
                composed_exprs.append(expr.get_composed())
                composed_values.append(params[expr._name])

        if len(composed_exprs) > 1:
            return SQL('SET ({}) = ({})').format(SQL(', ').join(composed_exprs), SQL(', ').join(composed_values))
        elif len(composed_exprs) == 1:
            return SQL('SET {} = {}').format(composed_exprs[0], composed_values[0])
        else:
            return Composed([])

    def FROM(self, value: FromValueType) -> UFrom:
        return UFrom(self.components, value)

    def WHERE(self, value: WhereValueType) -> UDWhere:
        return UDWhere(self.components, value)

    def RETURNING(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
