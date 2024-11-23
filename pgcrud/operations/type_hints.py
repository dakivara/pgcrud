from collections.abc import Sequence
from typing import Any, TypeVar

from pydantic import BaseModel

from pgcrud.col import Col
from pgcrud.operators.assign_operator import Assign
from pgcrud.operators.filter_operators import FilterOperator
from pgcrud.operators.join_operators import JoinOperator
from pgcrud.operators.sort_operators import SortOperator
from pgcrud.tab import Tab


__all__ = [
    'PydanticModel',
    'TableType',
    'JoinType',
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

JoinType = JoinOperator | Sequence[JoinOperator]
WhereType = FilterOperator
OrderByType = Col | SortOperator | Sequence[Col | SortOperator]

SelectType = str | Col | Sequence[str | Col] | type[BaseModel]
ReturnType = Any | tuple[Any, ...] | BaseModel

ValuesType = dict[str, Any] | BaseModel
SetType = Assign | dict[str, Any] | BaseModel | Sequence[Assign | dict[str, Any] | BaseModel]

AdditionalValuesType = dict[str, Any]
ExcludeType = str | Sequence[str]
ParamsType = Sequence[Any] | dict[str, Any] | BaseModel
