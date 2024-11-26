from collections.abc import Sequence
from typing import Any, Literal, TypeVar, Union, TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from pgcrud.col import Col
    from pgcrud.operators import FilterOperator, SortOperator, JoinOn
    from pgcrud.tab import Tab, SimpleTab


__all__ = [
    'PydanticModel',
    'SelectValueType',
    'FromValueType',
    'JoinValueType',
    'WhereValueType',
    'OrderByValueType',
    'InsertIntoValueType',
    'ValuesValueItemType',
    'ValuesValueType',
    'AdditionalValuesType',
    'ReturningValueType',
    'UpdateValueType',
    'ResultOneValueType',
    'ResultManyValueType',
    'HowValueType',
]


PydanticModel = TypeVar('PydanticModel', bound=BaseModel)
SelectValueType = Union['Col', Sequence['Col'], type[BaseModel]]
FromValueType = Union['Tab']
JoinValueType = Union['JoinOn', Sequence['JoinOn']]
WhereValueType = Union['FilterOperator']
OrderByValueType = Union['Col', 'SortOperator', Sequence[Union['Col', 'SortOperator']]]
InsertIntoValueType = Union['SimpleTab']
ValuesValueItemType = tuple[Any, ...] | dict[str, Any] | BaseModel
ValuesValueType = Sequence[ValuesValueItemType]
AdditionalValuesType = dict[str, Any]
ReturningValueType = Union['Col', Sequence['Col'], type[BaseModel]]
UpdateValueType = Union['SimpleTab']
ResultOneValueType = Any | tuple[Any, ...] | BaseModel
ResultManyValueType = list[Any] | list[tuple[Any, ...]] | list[BaseModel]
HowValueType = Literal['INNER', 'LEFT']
