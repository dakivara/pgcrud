from collections.abc import Sequence
from typing import Any, Literal, Union, TYPE_CHECKING
from typing_extensions import TypeVar


if TYPE_CHECKING:
    from pgcrud.expr import Expr, ReferenceExpr, TableReferenceExpr
    from pgcrud.operators import FilterOperator, SortOperator


__all__ = [
    'Row',
    'T',
    'ValidationType',
    'SelectValueType',
    'FromValueType',
    'WhereValueType',
    'GroupByValueType',
    'OrderByValueType',
    'InsertIntoValueType',
    'ValuesValueType',
    'AdditionalValuesType',
    'ReturningValueType',
    'UpdateValueType',
    'SetColsType',
    'SetValuesType',
    'SetValueType',
    'DeleteFromValueType',
    'HavingValueType',
    'WindowValueType',
    'UsingValueType',
    'PartitionByValueType',
    'HowValueType',
]


Row = TypeVar('Row', covariant=True, default=tuple[Any, ...])
T = TypeVar('T')

ValidationType = Literal['pydantic', 'msgspec', None]

SelectValueType = Union[Any, 'Expr', Sequence[Union[Any, 'Expr']]]
FromValueType = Union['Expr']
WhereValueType = Union['FilterOperator']
GroupByValueType = Union['Expr', Sequence['Expr']]
OrderByValueType = Union['Expr', 'SortOperator', Sequence[Union['Expr', 'SortOperator']]]
InsertIntoValueType = Union['TableReferenceExpr']
ValuesValueType = Any | Sequence[Any] | dict[str, Any]
AdditionalValuesType = dict[str, Any]
ReturningValueType = Union[Any, 'Expr', Sequence[Union[Any, 'Expr']]]
UpdateValueType = Union['ReferenceExpr']
SetColsType = Sequence['ReferenceExpr']
SetValuesType = Any | Sequence[Any] | dict[str, Any]
SetValueType = tuple[SetColsType, SetValuesType]
DeleteFromValueType = Union['ReferenceExpr']
HavingValueType = Union['FilterOperator']
WindowValueType = Union['Expr', Sequence['Expr']]
UsingValueType = Union['ReferenceExpr']
PartitionByValueType = Union['Expr', Sequence['Expr']]
HowValueType = Literal['INNER', 'LEFT', 'RIGHT', 'FULL', 'CROSS']
