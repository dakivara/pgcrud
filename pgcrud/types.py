from collections.abc import Sequence
from typing import Any, Literal, LiteralString, Union, TYPE_CHECKING
from typing_extensions import TypeVar


if TYPE_CHECKING:
    from pgcrud.query import Query


__all__ = [
    'Row',
    'T',
    'SequenceType',
    'ValidationType',
    'ParamsType',
    'QueryType'
]


Row = TypeVar('Row', covariant=True, default=tuple[Any, ...])
T = TypeVar('T')

SequenceType = list | tuple

ValidationType = Literal['pydantic', 'msgspec', None]
QueryType = Union[LiteralString, bytes, 'Query']
ParamsType = Union[Any, Sequence[Any], dict[str, Any]]
