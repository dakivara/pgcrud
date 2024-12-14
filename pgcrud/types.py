from collections.abc import Sequence
from typing import Any, Literal, Union, TYPE_CHECKING
from typing_extensions import TypeVar

from pydantic import BaseModel


if TYPE_CHECKING:
    from pgcrud.expr import Expr, ReferenceExpr, TableReferenceExpr
    from pgcrud.operators import FilterOperator, SortOperator


__all__ = [
    'Row',
    'T',
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
    'DeleteFromValueType',
    'HavingValueType',
    'WindowValueType',
    'UsingValueType',
    'PartitionByValueType',
    'HowValueType',
]


Row = TypeVar('Row', covariant=True, default=tuple[Any, ...])
T = TypeVar('T')
SelectValueType = Union['Expr', Sequence['Expr']]
FromValueType = Union['Expr']
WhereValueType = Union['FilterOperator']
GroupByValueType = Union['Expr', Sequence['Expr']]
OrderByValueType = Union['Expr', 'SortOperator', Sequence[Union['Expr', 'SortOperator']]]
InsertIntoValueType = Union['TableReferenceExpr']
ValuesValueItemType = Sequence[Any] | dict[str, Any] | BaseModel
ValuesValueType = Sequence[Any] | dict[str, Any] | BaseModel
AdditionalValuesType = dict[str, Any]
ReturningValueType = Union['Expr', Sequence['Expr']]
UpdateValueType = Union['ReferenceExpr']
SetColsType = Sequence['ReferenceExpr']
SetValuesType = Sequence[Any] | dict[str, Any] | BaseModel
DeleteFromValueType = Union['ReferenceExpr']
HavingValueType = Union['FilterOperator']
WindowValueType = Union['Expr', Sequence['Expr']]
UsingValueType = Union['ReferenceExpr']
PartitionByValueType = Union['Expr', Sequence['Expr']]
HowValueType = Literal['INNER', 'LEFT', 'RIGHT', 'FULL', 'CROSS']
