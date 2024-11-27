from collections.abc import Sequence
from typing import Any, Literal, TypeVar, Union, TYPE_CHECKING

from pydantic import BaseModel


if TYPE_CHECKING:
    from pgcrud.col import Col, SingleCol
    from pgcrud.operators import FilterOperator, SortOperator, JoinOn
    from pgcrud.tab import Tab, SimpleTab


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
    'ResultOneValueType',
    'ResultManyValueType',
    'HowValueType',
]


PydanticModel = TypeVar('PydanticModel', bound=BaseModel)
SelectValueType = Union['Col', Sequence['Col'], type[BaseModel]]
FromValueType = Union['Tab']
JoinValueType = Union['JoinOn', Sequence['JoinOn']]
WhereValueType = Union['FilterOperator']
GroupByValueType = Union['Col', Sequence['Col']]
OrderByValueType = Union['Col', 'SortOperator', Sequence[Union['Col', 'SortOperator']]]
InsertIntoValueType = Union['SimpleTab']
ValuesValueItemType = Sequence[Any] | dict[str, Any] | BaseModel
ValuesValueType = Sequence[ValuesValueItemType]
AdditionalValuesType = dict[str, Any]
ReturningValueType = Union['Col', Sequence['Col'], type[BaseModel]]
UpdateValueType = Union['Tab']
SetColsType = Sequence['SingleCol']
SetValueType = Sequence[Any] | dict[str, Any] | BaseModel
DeleteFromValueType = Union['Tab']
ResultOneValueType = Any | tuple[Any, ...] | BaseModel
ResultManyValueType = list[Any] | list[tuple[Any, ...]] | list[BaseModel]
HowValueType = Literal['INNER', 'LEFT', 'RIGHT', 'FULL', 'CROSS']
