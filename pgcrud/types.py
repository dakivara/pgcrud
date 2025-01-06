from collections.abc import Sequence
from typing import Any, Literal, LiteralString, Union, TYPE_CHECKING
from typing_extensions import TypeVar


if TYPE_CHECKING:
    from pgcrud.expressions import Expression, Identifier, TableIdentifier
    from pgcrud.filter_conditions import FilterCondition
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
    'SetValueType',
    'DeleteFromValueType',
    'HavingValueType',
    'WindowValueType',
    'UsingValueType',
]


Row = TypeVar('Row', covariant=True, default=tuple[Any, ...])
T = TypeVar('T')

ValidationType = Literal['pydantic', 'msgspec', None]
QueryType = Union[LiteralString, bytes, 'Query']
ParamsType = Union[Any, Sequence[Any], dict[str, Any]]

SelectValueType = Union[Any, 'Expression', 'Query', Sequence[Union[Any, 'Expression', 'Query']]]
FromValueType = Union['Expression']
WhereValueType = Union['FilterCondition']
GroupByValueType = Union[Any, 'Expression', 'Query', Sequence[Union[Any, 'Expression', 'Query']]]
HavingValueType = Union['FilterCondition']
WindowValueType = Union['Identifier']
OrderByValueType = Union[Any, 'Expression', 'Query', Sequence[Union[Any, 'Expression', 'Query']]]
InsertIntoValueType = Union['Identifier', 'TableIdentifier']
ValuesValueType = Any
ReturningValueType = Union[Any, 'Expression', Sequence[Union[Any, 'Expression']]]
UpdateValueType = Union['Identifier']
SetValueType = tuple[Union['Identifier', Sequence['Identifier']], Any]
DeleteFromValueType = Union['Identifier']
UsingValueType = Union['Expression']
AdditionalValuesType = dict[str, Any]
