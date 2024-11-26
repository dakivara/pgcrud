from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.operators.operator import Operator
from pgcrud.undefined import Undefined


if TYPE_CHECKING:
    from pgcrud.col import Col


__all__ = [
    'FilterOperator',
    'Equal',
    'NotEqual',
    'GreaterThan',
    'GreaterThanEqual',
    'LessThan',
    'LessThanEqual',
    'IsNull',
    'IsNotNull',
    'IsIn',
    'IsNotIn',
    'Intersection',
    'Union',
    # 'NotIn',
    # 'Like',
    # 'NotLike',
    # 'ILike',
    # 'NotILike'
]


@dataclass(repr=False)
class FilterOperator(Operator):

    @abstractmethod
    def __and__(self, other: 'FilterOperator') -> 'Intersection':
        pass

    @abstractmethod
    def __or__(self, other: 'FilterOperator') -> 'Union':
        pass

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    @abstractmethod
    def get_inner_composed(self) -> Composed:
        pass


@dataclass(repr=False)
class SingleFilterOperator(FilterOperator):

    def __and__(self, other: 'FilterOperator') -> 'Intersection':
        return Intersection([self] + other.operators) if isinstance(other, Intersection) else Intersection([self, other])

    def __or__(self, other: 'FilterOperator') -> 'Union':
        return Union([self] + other.operators) if isinstance(other, Union) else Union([self, other])

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    def get_inner_composed(self) -> Composed:
        return self.get_composed()


@dataclass(repr=False)
class ComparisonOperator(SingleFilterOperator):
    left: 'Col'
    right: 'Col'

    @property
    @abstractmethod
    def operator(self) -> SQL:
        pass

    def get_composed(self) -> Composed:
        if self.left and self.right:
            return SQL("{} {} {}").format(self.left.get_composed(), self.operator, self.right.get_composed())
        else:
            return Composed([])


@dataclass(repr=False)
class Equal(ComparisonOperator):

    @property
    def operator(self) -> SQL:
        return SQL('=')


@dataclass(repr=False)
class NotEqual(ComparisonOperator):

    @property
    def operator(self) -> SQL:
        return SQL('!=')


@dataclass(repr=False)
class GreaterThan(ComparisonOperator):

    @property
    def operator(self) -> SQL:
        return SQL('>')


@dataclass(repr=False)
class GreaterThanEqual(ComparisonOperator):

    @property
    def operator(self) -> SQL:
        return SQL('>=')


@dataclass(repr=False)
class LessThan(ComparisonOperator):

    @property
    def operator(self) -> SQL:
        return SQL('<')


@dataclass(repr=False)
class LessThanEqual(ComparisonOperator):

    @property
    def operator(self) -> SQL:
        return SQL('<=')


@dataclass(repr=False)
class IsIn(ComparisonOperator):

    @property
    def operator(self) -> SQL:
        return SQL('IN')


@dataclass(repr=False)
class IsNotIn(ComparisonOperator):

    @property
    def operator(self) -> SQL:
        return SQL('NOT IN')


@dataclass(repr=False)
class IsNull(SingleFilterOperator):
    col: 'Col'
    flag: bool = True

    def get_composed(self) -> Composed:
        if not self.col or self.flag is Undefined:
            return Composed([])
        elif self.flag:
            return SQL("{} IS NULL").format(self.col.get_composed())
        else:
            return SQL("{} IS NOT NULL").format(self.col.get_composed())


@dataclass(repr=False)
class IsNotNull(SingleFilterOperator):
    col: 'Col'
    flag: bool = True

    def get_composed(self) -> Composed:
        if not self.col or self.flag is Undefined:
            return Composed([])
        elif self.flag:
            return SQL("{} IS NOT NULL").format(self.col.get_composed())
        else:
            return SQL("{} IS NULL").format(self.col.get_composed())


@dataclass(repr=False)
class Intersection(FilterOperator):
    operators: list[FilterOperator]

    def __and__(self, other: 'FilterOperator') -> 'Intersection':
        if isinstance(other, Intersection):
            return Intersection(self.operators + other.operators)
        elif isinstance(other, Union):
            return Intersection([self, other])
        else:
            return Intersection(self.operators + [other])

    def __or__(self, other: 'FilterOperator') -> 'Union':
        return Union([self, other])

    def get_composed(self) -> Composed:
        return SQL(' AND ').join([operator.get_inner_composed() for operator in self.operators if operator])

    def get_inner_composed(self) -> Composed:
        composed = self.get_composed()
        if len(composed._obj) > 1:
            return Composed([SQL('('), composed, SQL(')')])
        else:
            return composed


@dataclass(repr=False)
class Union(FilterOperator):
    operators: list[FilterOperator]

    def __and__(self, other: 'FilterOperator') -> 'Intersection':
        return Intersection([self, other])

    def __or__(self, other: 'FilterOperator') -> 'Union':
        if isinstance(other, Union):
            return Union(self.operators + other.operators)
        elif isinstance(other, Intersection):
            return Union([self, other])
        else:
            return Union(self.operators + [other])

    def get_composed(self) -> Composed:
        return SQL(' OR ').join([operator.get_inner_composed() for operator in self.operators if operator])

    def get_inner_composed(self) -> Composed:
        composed = self.get_composed()
        if len(composed._obj) > 1:
            return Composed([SQL('('), composed, SQL(')')])
        else:
            return composed


# @dataclass
# class Like(FilterOperator):
#     value: str | None
#
#     def get_composed(self) -> Composed | None:
#         if self.value is not None:
#             return SQL("{} LIKE {}").format(Identifier(self.name), Literal(self.value))
#
#
# @dataclass
# class NotLike(FilterOperator):
#     value: str | None
#
#     def get_composed(self) -> Composed | None:
#         if self.value is not None:
#             return SQL("{} NOT LIKE {}").format(Identifier(self.name), Literal(self.value))
#
#
# @dataclass
# class ILike(FilterOperator):
#     value: str | None
#
#     def get_composed(self) -> Composed | None:
#         if self.value is not None:
#             return SQL("{} ILIKE {}").format(Identifier(self.name), Literal(self.value))
#
#
# @dataclass
# class NotILike(FilterOperator):
#     value: str | None
#
#     def get_composed(self) -> Composed | None:
#         if self.value is not None:
#             return SQL("{} NOT ILIKE {}").format(Identifier(self.name), Literal(self.value))
