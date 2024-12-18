from collections.abc import Sequence
from typing import Any, Literal, LiteralString, Union, TYPE_CHECKING
from typing_extensions import TypeVar


if TYPE_CHECKING:
    from pgcrud.expr import Expr, AliasExpr, ReferenceExpr, TableReferenceExpr
    from pgcrud.operators import FilterOperator, SortOperator
    from pgcrud.query import Query


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
QueryType = Union[LiteralString | bytes | 'Query']
ParamsType = Union[Any, Sequence[Any], dict[str, Any]]

SelectValueType = Union[Any, 'Expr', Sequence[Union[Any, 'Expr']]]
FromValueType = Union['Expr']
WhereValueType = Union['FilterOperator']
GroupByValueType = Union[Any, 'Expr', Sequence[Union[Any, 'Expr']]]
OrderByValueType = Union[Any, 'Expr', 'SortOperator', Sequence[Union[Any, 'Expr', 'SortOperator']]]
InsertIntoValueType = Union['TableReferenceExpr']
ValuesValueType = Any | Sequence[Any] | dict[str, Any]
AdditionalValuesType = dict[str, Any]
ReturningValueType = Union[Any, 'Expr', Sequence[Union[Any, 'Expr']]]
UpdateValueType = Union['ReferenceExpr']
SetColsType = Union['ReferenceExpr', Sequence['ReferenceExpr']]
SetValuesType = Any | Sequence[Any] | dict[str, Any]
SetValueType = tuple[SetColsType, SetValuesType]
DeleteFromValueType = Union['ReferenceExpr']
HavingValueType = Union['FilterOperator']
WindowValueType = Union['AliasExpr', Sequence['AliasExpr']]
UsingValueType = Union['Expr']
PartitionByValueType = Union['Expr', Sequence['Expr']]
HowValueType = Literal['INNER', 'LEFT', 'RIGHT', 'FULL', 'CROSS']
