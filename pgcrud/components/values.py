from dataclasses import dataclass
from typing import Sequence, TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.returning import Returning
from pgcrud.types import ReturningValueType, ValuesValueType, AdditionalValuesType


if TYPE_CHECKING:
    from pgcrud.col import SingleCol


__all__ = ['Values']


@dataclass
class Values(Component):
    value: ValuesValueType
    additional_values: AdditionalValuesType

    def get_single_composed(self) -> Composed:

        composed_list = []

        for vals in self.value:
            if isinstance(vals, Sequence):
                composed_list.append(SQL('({})').format(SQL(', ').join([val for _, val in zip(self.get_cols(), vals, strict=True)])))
            elif isinstance(vals, dict):
                params = self.additional_values.copy()
                params.update(vals)
                composed_list.append(SQL('({})').format(SQL(', ').join([params[col.name] for col in self.get_cols()])))
            else:
                params = self.additional_values.copy()
                params.update(vals.model_dump(by_alias=True))
                composed_list.append(SQL('({})').format(SQL(', ').join([params[col.name] for col in self.get_cols()])))

        if composed_list:
            return SQL('VALUES {}').format(SQL(', ').join(composed_list))
        else:
            return Composed([])

    def get_cols(self) -> tuple['SingleCol', ...]:
        if self.prev_components and hasattr(self.prev_components[-1], 'get_cols'):
            return getattr(self.prev_components[-1], 'get_cols')()
        else:
            return ()

    def returning(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
