from collections.abc import Sequence
from typing import Any, TypeVar

from pydantic import BaseModel

from pgcrud._col import Col
from pgcrud._operators.assign_operator import Assign
from pgcrud._operators.filter_operators import FilterOperator
from pgcrud._operators.sort_operators import SortOperator
from pgcrud._tab import Tab


__all__ = [
    'PydanticModel',
    'TableType',
    'WhereType',
    'OrderByType',
    'SelectType',
    'ReturnType',
    'ValuesType',
    'SetType',
    'AdditionalValuesType',
    'ExcludeType',
    'ParamsType',
]


PydanticModel = TypeVar('PydanticModel', bound=BaseModel)

TableType = str | Tab

WhereType = FilterOperator
OrderByType = Col | SortOperator | Sequence[Col | SortOperator]

SelectType = str | Col | Sequence[str | Col] | type[BaseModel]
ReturnType = Any | tuple[Any, ...] | BaseModel

ValuesType = dict[str, Any] | BaseModel
SetType = Assign | dict[str, Any] | BaseModel | Sequence[Assign | dict[str, Any] | BaseModel]

AdditionalValuesType = dict[str, Any]
ExcludeType = str | Sequence[str]
ParamsType = Sequence[Any] | dict[str, Any] | BaseModel
