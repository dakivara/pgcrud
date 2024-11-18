from abc import abstractmethod

from dataclasses import dataclass
from typing import Any, Literal as LiteralType

from psycopg.sql import SQL, Composed, Identifier, Literal


__all__ = [
    'FilterOperator',
    'Equal',
    'NotEqual',
    'LargerThan',
    'LargerThanEqual',
    'LessThan',
    'LessThanEqual',
    'IsNull',
    'In',
    'NotIn',
    'Like',
    'NotLike',
    'ILike',
    'NotILike'
]


@dataclass
class FilterOperator:
    name: str

    @abstractmethod
    def get_composed(self) -> Composed | None:
        raise NotImplementedError


@dataclass
class Equal(FilterOperator):
    value: Any

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} = {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class NotEqual(FilterOperator):
    value: Any

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} != {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class LargerThan(FilterOperator):
    value: Any

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} > {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class LargerThanEqual(FilterOperator):
    value: Any

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} >= {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class LessThan(FilterOperator):
    value: Any

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} < {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class LessThanEqual(FilterOperator):
    value: Any

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} <= {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class IsNull(FilterOperator):
    value: bool | LiteralType[0, 1] | None

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            if self.value:
                return SQL("{} IS NULL").format(Identifier(self.name))
            else:
                return SQL("{} IS NOT NULL").format(Identifier(self.name))


@dataclass
class In(FilterOperator):
    value: list[Any]

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} IN {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class NotIn(FilterOperator):
    value: list[Any]

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} NOT IN {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class Like(FilterOperator):
    value: str | None

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} LIKE {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class NotLike(FilterOperator):
    value: str | None

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} NOT LIKE {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class ILike(FilterOperator):
    value: str | None

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} ILIKE {}").format(Identifier(self.name), Literal(self.value))


@dataclass
class NotILike(FilterOperator):
    value: str | None

    def get_composed(self) -> Composed | None:
        if self.value is not None:
            return SQL("{} NOT ILIKE {}").format(Identifier(self.name), Literal(self.value))
