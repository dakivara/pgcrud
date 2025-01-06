from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Sequence


if TYPE_CHECKING:
    from pgcrud.expressions import Expression, Undefined


__all__ = [
    'FilterCondition',
    'ComparisonFilterCondition',
    'Equal',
    'NotEqual',
    'GreatThan',
    'GreaterThanEqual',
    'LessThan',
    'LessThanEqual',
    'In',
    'NotIn',
    'IsNull',
    'IsNotNull',
    'Between',
    'ComposedFilterCondition',
    'Intersection',
    'Union',
]


class FilterCondition:

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __bool__(self) -> bool:
        pass

    def __repr__(self):
        return str(self)

    def __and__(self, other: FilterCondition) -> Intersection:
        return Intersection(*self.and_args, *other.and_args)

    def __or__(self, other: FilterCondition) -> Union:
        return Union(*self.or_args, *other.or_args)

    @property
    def and_args(self) -> tuple[FilterCondition, ...]:
        return (self,) if self else ()

    @property
    def and_str(self) -> str:
        return str(self)

    @property
    def or_args(self) -> tuple[FilterCondition, ...]:
        return (self,) if self else ()

    @property
    def or_str(self) -> str:
        return str(self)


class ComparisonFilterCondition(FilterCondition):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self):
        if self:
            return f'{self.left} {self.operator} {self.right}'
        else:
            return ''

    def __bool__(self) -> bool:
        return bool(self.left) and bool(self.right)

    @property
    @abstractmethod
    def operator(self) -> str:
        pass


class Equal(ComparisonFilterCondition):

    @property
    def operator(self) -> str:
        return '='


class NotEqual(ComparisonFilterCondition):

    @property
    def operator(self) -> str:
        return '<>'


class GreatThan(ComparisonFilterCondition):

    @property
    def operator(self) -> str:
        return '>'


class GreaterThanEqual(ComparisonFilterCondition):

    @property
    def operator(self) -> str:
        return '>='


class LessThan(ComparisonFilterCondition):

    @property
    def operator(self) -> str:
        return '<'


class LessThanEqual(ComparisonFilterCondition):

    @property
    def operator(self) -> str:
        return '<='


class In(FilterCondition):

    def __init__(
            self,
            left: Expression,
            right: Sequence[Expression],
    ):
        self.left = left
        self.right = right

    def __str__(self):
        if self:
            return f"{self.left} IN ({', '.join([str(expression) for expression in self.right if expression])})"
        else:
            return ''

    def __bool__(self) -> bool:
        return any(self.right)


class NotIn(FilterCondition):

    def __init__(
            self,
            left: Expression,
            right: Sequence[Expression],
    ):
        self.left = left
        self.right = right

    def __str__(self):
        if self:
            return f"{self.left} NOT IN ({', '.join([str(expression) for expression in self.right if expression])})"
        else:
            return ''

    def __bool__(self) -> bool:
        return any(self.right)


class IsNull(FilterCondition):

    def __init__(
            self,
            expr: Expression,
            flag: bool | Undefined,
    ):
        self.expr = expr
        self.flag = flag

    def __str__(self):
        if self:
            if self.flag:
                return f'{self.expr} IS NULL'
            else:
                return f'{self.expr} IS NOT NULL'
        else:
            return ''

    def __bool__(self) -> bool:
        return isinstance(self.flag, bool)


class IsNotNull(FilterCondition):

    def __init__(
            self,
            expr: Expression,
            flag: bool | Undefined,
    ):
        self.expr = expr
        self.flag = flag

    def __str__(self):
        if self:
            if self.flag:
                return f'{self.expr} IS NOT NULL'
            else:
                return f'{self.expr} IS NULL'
        else:
            return ''

    def __bool__(self) -> bool:
        return isinstance(self.flag, bool)


class Between(FilterCondition):

    def __init__(
            self,
            expr: Expression,
            start: Expression,
            end: Expression,
    ):
        self.expr = expr
        self.start = start
        self.end = end

    def __str__(self):
        if self:
            return f"{self.expr} BETWEEN {self.start} AND {self.end}"
        else:
            return ''

    def __bool__(self) -> bool:
        return bool(self.start) and bool(self.end)


class ComposedFilterCondition(FilterCondition):

    def __init__(
            self,
            *args: FilterCondition,
    ):
        self.args = args

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __bool__(self) -> bool:
        return len(self.args) > 0

    @property
    @abstractmethod
    def operator(self) -> str:
        pass


class Intersection(ComposedFilterCondition):

    def __str__(self) -> str:
        return self.operator.join([expr.and_str for expr in self.args if expr])

    @property
    def and_args(self) -> tuple[FilterCondition, ...]:
        return self.args

    @property
    def or_str(self) -> str:
        return f'({self})' if len(self.args) > 1 else str(self)

    @property
    def operator(self) -> str:
        return ' AND '


class Union(ComposedFilterCondition):

    def __str__(self) -> str:
        return self.operator.join([expr.or_str for expr in self.args if expr])

    @property
    def and_str(self) -> str:
        return f'({self})' if len(self.args) > 1 else str(self)

    @property
    def or_args(self) -> tuple[FilterCondition, ...]:
        return self.args

    @property
    def operator(self) -> str:
        return ' OR '
