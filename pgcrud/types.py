from collections.abc import Sequence
from typing import Any, Literal, TypeVar, Union, TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from pgcrud.expr import Expr, ReferenceExpr, TableReferenceExpr
    from pgcrud.operators import FilterOperator, SortOperator, JoinOn


__all__ = [
    'PydanticModel',
    'SelectValueType',
    'FromValueType',
    'JoinValueType',
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
JoinValueType = Union['JoinOn', Sequence['JoinOn']]
WhereValueType = Union['FilterOperator']
GroupByValueType = Union['Expr', Sequence['Expr']]
OrderByValueType = Union['Expr', 'SortOperator', Sequence[Union['Expr', 'SortOperator']]]
InsertIntoValueType = Union['TableReferenceExpr']
ValuesValueItemType = Sequence[Any] | dict[str, Any] | BaseModel
ValuesValueType = Sequence[ValuesValueItemType]
AdditionalValuesType = dict[str, Any]
ReturningValueType = Union['Expr', Sequence['Expr'], type[BaseModel]]
UpdateValueType = Union['ReferenceExpr']
SetColsType = Sequence['ReferenceExpr']
SetValueType = Sequence[Any] | dict[str, Any] | BaseModel
DeleteFromValueType = Union['ReferenceExpr']
HavingValueType = Union['FilterOperator']
UsingValueType = Union['ReferenceExpr']
ResultOneValueType = Any | tuple[Any, ...] | BaseModel
ResultManyValueType = list[Any] | list[tuple[Any, ...]] | list[BaseModel]
HowValueType = Literal['INNER', 'LEFT', 'RIGHT', 'FULL', 'CROSS']
