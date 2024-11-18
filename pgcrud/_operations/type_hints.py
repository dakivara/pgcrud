from collections.abc import Sequence
from typing import Any, TypeVar

from pydantic import BaseModel

from pgcrud._star import _TSTAR, _DSTAR
from pgcrud.operators.filter_operators import FilterOperator
from pgcrud.operators.logical_operators import LogicalOperator
from pgcrud.operators.sort_operators import SortOperator


__all__ = [
    'OutputModel',
    'InputModel',
    'WhereType',
    'OrderByType',
    'SelectType',
    'ReturnType',
    'ValuesType',
    'SetType',
    'ExcludeType',
    'ParamsType',
]


InputModel = TypeVar('InputModel', bound=BaseModel)
OutputModel = TypeVar('OutputModel', bound=BaseModel)

WhereType = FilterOperator | LogicalOperator | Sequence[LogicalOperator | FilterOperator]
OrderByType = SortOperator | Sequence[SortOperator]

SelectType = str | tuple[str] | _TSTAR | list[str] | _DSTAR | type[OutputModel]
ReturnType = Any | tuple[Any] | dict[str, Any] | OutputModel

ValuesType = Sequence[tuple[str, Any]] | dict[str, Any] | InputModel
SetType = Sequence[tuple[str, Any]] | dict[str, Any] | InputModel

ExcludeType = str | Sequence[str]
ParamsType = tuple[Any] | dict[str, Any] | InputModel
