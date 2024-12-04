from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed

from pgcrud.operators.operator import Operator
from pgcrud.undefined import Undefined


if TYPE_CHECKING:
    from pgcrud.expr import Expr


__all__ = [
    'FilterOperator',
    'UndefinedFilter',
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

    def __bool__(self) -> bool:
        return not isinstance(self, UndefinedFilter)

    @abstractmethod
    def __and__(self, other: 'FilterOperator') -> 'FilterOperator':
        pass

    @abstractmethod
    def __or__(self, other: 'FilterOperator') -> 'FilterOperator':
        pass

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    @abstractmethod
    def get_inner_composed(self) -> Composed:
        pass


@dataclass(repr=False)
class UndefinedFilter(FilterOperator):

    def __and__(self, other: 'FilterOperator') -> 'FilterOperator':
        return other

    def __or__(self, other: 'FilterOperator') -> 'FilterOperator':
        return other

    def get_composed(self) -> Composed:
        return Composed([])

    def get_inner_composed(self) -> Composed:
        return self.get_composed()


@dataclass(repr=False)
class ScalarFilterOperator(FilterOperator):

    def __and__(self, other: 'FilterOperator') -> 'FilterOperator':
        if isinstance(other, UndefinedFilter):
            return self
        elif isinstance(other, Intersection):
            return Intersection([self] + other.operators)
        else:
            return Intersection([self, other])

    def __or__(self, other: 'FilterOperator') -> 'FilterOperator':
        if isinstance(other, UndefinedFilter):
            return self
        elif isinstance(other, Union):
            return Union([self] + other.operators)
        else:
            return Union([self, other])

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    def get_inner_composed(self) -> Composed:
        return self.get_composed()


@dataclass(repr=False)
class ComparisonOperator(ScalarFilterOperator):
    left: 'Expr'
    right: 'Expr'

    @property
    @abstractmethod
    def operator(self) -> SQL:
        pass

    def get_composed(self) -> Composed:
        return SQL("{} {} {}").format(self.left.get_composed(), self.operator, self.right.get_composed())


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
class IsNull(ScalarFilterOperator):
    expr: 'Expr'
    flag: bool

    def get_composed(self) -> Composed:
        if self.flag:
            return SQL("{} IS NULL").format(self.expr.get_composed())
        else:
            return SQL("{} IS NOT NULL").format(self.expr.get_composed())


@dataclass(repr=False)
class IsNotNull(ScalarFilterOperator):
    expr: 'Expr'
    flag: bool | type[Undefined] = True

    def get_composed(self) -> Composed:
        if self.flag:
            return SQL("{} IS NOT NULL").format(self.expr.get_composed())
        else:
            return SQL("{} IS NULL").format(self.expr.get_composed())


@dataclass(repr=False)
class CompositeFilterOperator(FilterOperator):
    operators: list[FilterOperator]

    @abstractmethod
    def __and__(self, other: 'FilterOperator') -> 'FilterOperator':
        pass

    @abstractmethod
    def __or__(self, other: 'FilterOperator') -> 'FilterOperator':
        pass

    @property
    @abstractmethod
    def operator(self) -> SQL:
        pass

    def get_composed(self) -> Composed:
        return self.operator.join([operator.get_inner_composed() for operator in self.operators])

    def get_inner_composed(self) -> Composed:
        composed = self.get_composed()
        if len(composed._obj) > 1:
            return Composed([SQL('('), composed, SQL(')')])
        else:
            return composed


@dataclass(repr=False)
class Intersection(CompositeFilterOperator):

    def __and__(self, other: 'FilterOperator') -> 'FilterOperator':
        if isinstance(other, UndefinedFilter):
            return self
        elif isinstance(other, Intersection):
            return Intersection(self.operators + other.operators)
        elif isinstance(other, Union):
            return Intersection([self, other])
        else:
            return Intersection(self.operators + [other])

    def __or__(self, other: 'FilterOperator') -> 'FilterOperator':
        if isinstance(other, UndefinedFilter):
            return UndefinedFilter()
        else:
            return Union([self, other])

    @property
    def operator(self) -> SQL:
        return SQL(' AND ')


@dataclass(repr=False)
class Union(FilterOperator):
    operators: list[FilterOperator]

    def __and__(self, other: 'FilterOperator') -> 'FilterOperator':
        if isinstance(other, UndefinedFilter):
            return self
        else:
            return Intersection([self, other])

    def __or__(self, other: 'FilterOperator') -> 'FilterOperator':
        if isinstance(other, UndefinedFilter):
            return self
        elif isinstance(other, Union):
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
