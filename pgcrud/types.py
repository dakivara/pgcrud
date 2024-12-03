from collections.abc import Sequence
from typing import Any, Literal, TypeVar, Union, TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from pgcrud.expr import Expr, ReferenceExpr, TableReferenceExpr
    from pgcrud.operators import FilterOperator, SortOperator


__all__ = [
    'PydanticModel',
    'SelectValueType',
    'FromValueType',
    'WhereValueType',
    'GroupByValueType',
    'OrderByValueType',
    'InsertIntoValueType',
    'ValuesValueItemType',
    'ValuesValueType',
    'AdditionalValuesType',
    'ReturningValueType',
    'UpdateValueType',
    'SetColsType',
    'SetValuesType',
    'SetValueType',
    'DeleteFromValueType',
    'HavingValueType',
    'UsingValueType',
    'ResultOneValueType',
    'ResultManyValueType',
    'HowValueType',
]


PydanticModel = TypeVar('PydanticModel', bound=BaseModel)
SelectValueType = Union['Expr', Sequence['Expr'], type[BaseModel]]
FromValueType = Union['Expr']
WhereValueType = Union['FilterOperator']
GroupByValueType = Union['Expr', Sequence['Expr']]
OrderByValueType = Union['Expr', 'SortOperator', Sequence[Union['Expr', 'SortOperator']]]
InsertIntoValueType = Union['TableReferenceExpr']
ValuesValueItemType = Sequence[Any] | dict[str, Any] | BaseModel
ValuesValueType = Sequence[Any] | dict[str, Any] | BaseModel
AdditionalValuesType = dict[str, Any]
ReturningValueType = Union['Expr', Sequence['Expr'], type[BaseModel]]
UpdateValueType = Union['ReferenceExpr']
SetColsType = Sequence['ReferenceExpr']
SetValuesType = Sequence[Any] | dict[str, Any] | BaseModel
SetValueType = tuple[SetColsType, SetValuesType]
DeleteFromValueType = Union['ReferenceExpr']
HavingValueType = Union['FilterOperator']
UsingValueType = Union['ReferenceExpr']
ResultOneValueType = Any | tuple[Any, ...] | BaseModel
ResultManyValueType = list[Any] | list[tuple[Any, ...]] | list[BaseModel]
HowValueType = Literal['INNER', 'LEFT', 'RIGHT', 'FULL', 'CROSS']
