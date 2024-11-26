from dataclasses import dataclass
from typing import Any

from psycopg.sql import SQL, Composed

from pgcrud.components.component import Component
from pgcrud.components.returning import Returning
from pgcrud.types import ReturningValueType, ValuesValueType, AdditionalValuesType


__all__ = ['Values']


@dataclass
class Values(Component):
    value: ValuesValueType
    additional_values: AdditionalValuesType

    def get_single_composed(self) -> Composed:

        composed_list = []

        for v in self.value:
            if isinstance(v, tuple):
                composed_list.append(self.get_positional_placeholder().format(*v))
            elif isinstance(v, dict):
                params = self.additional_values.copy()
                params.update(v)
                composed_list.append(self.get_named_placeholder().format(**params))
            else:
                params = self.additional_values.copy()
                params.update(v.model_dump(by_alias=True))
                composed_list.append(self.get_named_placeholder().format(**params))

        if composed_list:
            return SQL('VALUES {}').format(SQL(', ').join(composed_list))
        else:
            return Composed([])

    def get_positional_placeholder(self) -> SQL:
        if self.prev_components and hasattr(self.prev_components[-1], 'get_positional_placeholder'):
            return getattr(self.prev_components[-1], 'get_positional_placeholder')()
        else:
            return SQL('()')

    def get_named_placeholder(self) -> SQL:
        if self.prev_components and hasattr(self.prev_components[-1], 'get_named_placeholder'):
            return getattr(self.prev_components[-1], 'get_named_placeholder')()
        else:
            return SQL('()')

    def returning(self, value: ReturningValueType) -> Returning:
        return Returning(self.components, value)
