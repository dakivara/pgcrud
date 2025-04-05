from __future__ import annotations

from abc import abstractmethod
from typing import Any, Self, TYPE_CHECKING

from psycopg.sql import Identifier, Literal
from pgcrud.utils import ensure_seq


if TYPE_CHECKING:
    from pgcrud.query import Query


__all__ = [
    'make_expr',
    'Expression',

    'LiteralExpression',
    'IdentifierExpression',
    'UndefinedExpression',
    'PlaceholderExpression',
    'UnboundedExpression',
    'CurrentRowExpression',
    'DefaultExpression',
    'ExcludedExpression',

    'ArithmeticOperationExpression',
    'AddOperationExpression',
    'SubtractOperationExpression',
    'MultiplyOperationExpression',
    'DivideOperationExpression',
    'PowerOperationExpression',

    'ComparisonOperationExpression',
    'EqualOperationExpression',
    'NotEqualOperationExpression',
    'GreatThanOperationExpression',
    'GreaterThanEqualOperationExpression',
    'LessThanOperationExpression',
    'LessThanEqualOperationExpression',

    'LogicalOperationExpression',
    'IntersectionOperationExpression',
    'UnionOperationExpression',

    'ClauseExpression',
    'AsClauseExpression',
    'AscClauseExpression',
    'DescClauseExpression',
    'IsClauseExpression',
    'IsNotClauseExpression',
    'InClauseExpression',
    'NotInClauseExpression',
    'BetweenClauseExpression',
    'FilterClauseExpression',
    'JoinClauseExpression',
    'LeftJoinClauseExpression',
    'RightJoinClauseExpression',
    'InnerJoinClauseExpression',
    'FullJoinClauseExpression',
    'CrossJoinClauseExpression',
    'OnClauseExpression',
    'OverClauseExpression',
    'PrecedingClauseExpression',
    'FollowingClauseExpression',

    'QueryExpression',
]


def make_expr(value: Any) -> Expression:
    return getattr(value, '_expr', LiteralExpression(value))


class Expression:

    @abstractmethod
    def __str__(self) -> str:
        pass

    def __bool__(self) -> bool:
        return True

    def __repr__(self):
        return str(self)

    def __add__(self, other: Any) -> AddOperationExpression:
        return AddOperationExpression(self, make_expr(other))

    def __radd__(self, other: Any) -> AddOperationExpression:
        return LiteralExpression(other) + self

    def __sub__(self, other: Any) -> SubtractOperationExpression:
        return SubtractOperationExpression(self, make_expr(other))

    def __rsub__(self, other: Any) -> SubtractOperationExpression:
        return LiteralExpression(other) - self

    def __mul__(self, other: Any) -> MultiplyOperationExpression:
        return MultiplyOperationExpression(self, make_expr(other))

    def __rmul__(self, other: Any) -> MultiplyOperationExpression:
        return LiteralExpression(other) * self

    def __truediv__(self, other: Any) -> DivideOperationExpression:
        return DivideOperationExpression(self, make_expr(other))

    def __rtruediv__(self, other: Any) -> DivideOperationExpression:
        return LiteralExpression(other) / self

    def __pow__(self, other: Any) -> PowerOperationExpression:
        return PowerOperationExpression(self, make_expr(other))

    def __rpow__(self, other: Any) -> PowerOperationExpression:
        return LiteralExpression(other) ** self

    def __eq__(self, other: Any) -> EqualOperationExpression:  # type: ignore
        return EqualOperationExpression(self, make_expr(other))

    def __ne__(self, other: Any) -> NotEqualOperationExpression:  # type: ignore
        return NotEqualOperationExpression(self, make_expr(other))

    def __gt__(self, other: Any) -> GreatThanOperationExpression:
        return GreatThanOperationExpression(self, make_expr(other))

    def __ge__(self, other: Any) -> GreaterThanEqualOperationExpression:
        return GreaterThanEqualOperationExpression(self, make_expr(other))

    def __lt__(self, other: Any) -> LessThanOperationExpression:
        return LessThanOperationExpression(self, make_expr(other))

    def __le__(self, other: Any) -> LessThanEqualOperationExpression:
        return LessThanEqualOperationExpression(self, make_expr(other))

    def __and__(self, other: Any) -> IntersectionOperationExpression:
        return IntersectionOperationExpression(self, make_expr(other))

    def __rand__(self, other: Any) -> IntersectionOperationExpression:
        return LiteralExpression(other) & self

    def __or__(self, other: Any) -> UnionOperationExpression:
        return UnionOperationExpression(self, make_expr(other))

    def __ror__(self, value: Any) -> UnionOperationExpression:
        return LiteralExpression(value) | self

    def AS(self, value: Any) -> AsClauseExpression:
        return AsClauseExpression(self, make_expr(value))

    def ASC(self, flag: bool | UndefinedExpression = True) -> AscClauseExpression:
        return AscClauseExpression(self, flag)

    def DESC(self, flag: bool | UndefinedExpression = True) -> DescClauseExpression:
        return DescClauseExpression(self, flag)

    def IS(self, value: Any) -> IsClauseExpression:
        return IsClauseExpression(self, make_expr(value))

    def IS_NOT(self, value: Any) -> IsNotClauseExpression:
        return IsNotClauseExpression(self, make_expr(value))

    def IN(self, values: list[Any]) -> InClauseExpression:
        return InClauseExpression(self, [make_expr(value) for value in values])

    def NOT_IN(self, values: list[Any]) -> NotInClauseExpression:
        return NotInClauseExpression(self, [make_expr(value) for value in values])

    def BETWEEN(self, start: Any, end: Any) -> BetweenClauseExpression:
        return BetweenClauseExpression(self, make_expr(start), make_expr(end))

    def FILTER(self, value: Any) -> FilterClauseExpression:
        return FilterClauseExpression(self, make_expr(value))

    def JOIN(self, value: Any) -> JoinClauseExpression:
        return JoinClauseExpression(self, make_expr(value))

    def LEFT_JOIN(self, value: Any) -> LeftJoinClauseExpression:
        return LeftJoinClauseExpression(self, make_expr(value))

    def RIGHT_JOIN(self, value: Any) -> RightJoinClauseExpression:
        return RightJoinClauseExpression(self, make_expr(value))

    def INNER_JOIN(self, value: Any) -> InnerJoinClauseExpression:
        return InnerJoinClauseExpression(self, make_expr(value))

    def FULL_JOIN(self, value: Any) -> FullJoinClauseExpression:
        return FullJoinClauseExpression(self, make_expr(value))

    def CROSS_JOIN(self, value: Any) -> CrossJoinClauseExpression:
        return CrossJoinClauseExpression(self, make_expr(value))

    def ON(self, value: Any) -> OnClauseExpression:
        return OnClauseExpression(self, make_expr(value))

    def OVER(self, value: Any) -> OverClauseExpression:
        return OverClauseExpression(self, make_expr(value))

    @property
    def PRECEDING(self) -> PrecedingClauseExpression:
        return PrecedingClauseExpression(self)

    @property
    def FOLLOWING(self) -> FollowingClauseExpression:
        return FollowingClauseExpression(self)

    @property
    def _expr(self) -> Self:
        return self


class LiteralExpression(Expression):

    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return Literal(self.value).as_string()


class IdentifierExpressionType(type):

    def __getattr__(cls, item) -> IdentifierExpression:
        return cls(item)


class IdentifierExpression(Expression, metaclass=IdentifierExpressionType):

    def __init__(
            self,
            name: str,
            parent: Expression | None = None,
    ):
        self._name = name
        self._parent = parent
        self._identifier = Identifier(name).as_string()
        self._columns = []

    def __call__(self, item: str) -> IdentifierExpression:
        return IdentifierExpression(item, self)

    def __getattr__(self, item: str) -> IdentifierExpression:
        return IdentifierExpression(item, self)

    def __getitem__(self, item: IdentifierExpression | tuple[IdentifierExpression, ...]) -> Self:
        self._columns += list(ensure_seq(item))
        return self

    def __str__(self) -> str:

        base_str = self._identifier

        if self._columns:
            base_str += f" ({', '.join(str(column) for column in self._columns)})"

        if self._parent:
            base_str = f"{self._parent}.{base_str}"

        return base_str


class UndefinedExpression(Expression):

    def __str__(self) -> str:
        return ''


class PlaceholderExpression(Expression):

    def __init__(
            self,
            name: str | None = None,
    ) -> None:
        self.name = name

    @property
    def _base_str(self) -> str:
        if self.name:
            return f'%({self.name})s'
        else:
            return '%s'


class UnboundedExpression(Expression):

    def __str__(self) -> str:
        return 'UNBOUNDED'


class CurrentRowExpression(Expression):

    def __str__(self) -> str:
        return 'CURRENT ROW'


class DefaultExpression(Expression):

    def __str__(self) -> str:
        return 'DEFAULT'


class ExcludedExpression(Expression):

    def __str__(self) -> str:
        return 'EXCLUDED'

    def __call__(self, item: str) -> IdentifierExpression:
        return IdentifierExpression(item, self)

    def __getattr__(self, item: str) -> IdentifierExpression:
        return IdentifierExpression(item, self)


class ArithmeticOperationExpression(Expression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left_str} {self.operator} {self.right_str}'

    @property
    @abstractmethod
    def operator(self) -> str:
        pass

    @property
    @abstractmethod
    def left_str(self) -> str:
        pass

    @property
    @abstractmethod
    def right_str(self) -> str:
        pass


class AddOperationExpression(ArithmeticOperationExpression):

    @property
    def operator(self) -> str:
        return '+'

    @property
    def left_str(self) -> str:
        if isinstance(self.left, (SubtractOperationExpression, MultiplyOperationExpression, DivideOperationExpression, PowerOperationExpression)):
            return f'({self.left})'
        else:
            return str(self.left)

    @property
    def right_str(self) -> str:
        if isinstance(self.right, (SubtractOperationExpression, MultiplyOperationExpression, DivideOperationExpression, PowerOperationExpression)):
            return f'({self.right})'
        else:
            return str(self.right)


class SubtractOperationExpression(ArithmeticOperationExpression):

    @property
    def operator(self) -> str:
        return '-'

    @property
    def left_str(self) -> str:
        if isinstance(self.left, (AddOperationExpression, MultiplyOperationExpression, DivideOperationExpression, PowerOperationExpression)):
            return f'({self.left})'
        else:
            return str(self.left)

    @property
    def right_str(self) -> str:
        if isinstance(self.right, ArithmeticOperationExpression):
            return f'({self.right})'
        else:
            return str(self.right)


class MultiplyOperationExpression(ArithmeticOperationExpression):

    @property
    def operator(self) -> str:
        return '*'

    @property
    def left_str(self) -> str:
        if isinstance(self.left, (AddOperationExpression, SubtractOperationExpression, DivideOperationExpression, PowerOperationExpression)):
            return f'({self.left})'
        else:
            return str(self.left)

    @property
    def right_str(self) -> str:
        if isinstance(self.right, (AddOperationExpression, SubtractOperationExpression, DivideOperationExpression, PowerOperationExpression)):
            return f'({self.right})'
        else:
            return str(self.right)


class DivideOperationExpression(ArithmeticOperationExpression):

    @property
    def operator(self) -> str:
        return '/'

    @property
    def left_str(self) -> str:
        if isinstance(self.left, (AddOperationExpression, SubtractOperationExpression, MultiplyOperationExpression, PowerOperationExpression)):
            return f'({self.left})'
        else:
            return str(self.left)

    @property
    def right_str(self) -> str:
        if isinstance(self.right, ArithmeticOperationExpression):
            return f'({self.right})'
        else:
            return str(self.right)


class PowerOperationExpression(ArithmeticOperationExpression):

    @property
    def operator(self) -> str:
        return '^'

    @property
    def left_str(self) -> str:
        if isinstance(self.left, ArithmeticOperationExpression):
            return f'({self.left})'
        else:
            return str(self.left)

    @property
    def right_str(self) -> str:
        if isinstance(self.right, (AddOperationExpression, SubtractOperationExpression, MultiplyOperationExpression, DivideOperationExpression)):
            return f'({self.right})'
        else:
            return str(self.right)


class ComparisonOperationExpression(Expression):

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


class EqualOperationExpression(ComparisonOperationExpression):

    @property
    def operator(self) -> str:
        return '='


class NotEqualOperationExpression(ComparisonOperationExpression):

    @property
    def operator(self) -> str:
        return '<>'


class GreatThanOperationExpression(ComparisonOperationExpression):

    @property
    def operator(self) -> str:
        return '>'


class GreaterThanEqualOperationExpression(ComparisonOperationExpression):

    @property
    def operator(self) -> str:
        return '>='


class LessThanOperationExpression(ComparisonOperationExpression):

    @property
    def operator(self) -> str:
        return '<'


class LessThanEqualOperationExpression(ComparisonOperationExpression):

    @property
    def operator(self) -> str:
        return '<='


class LogicalOperationExpression(Expression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __bool__(self):
        return bool(self.left) or bool(self.right)

    def __str__(self) -> str:
        if self.left and self.right:
            return f'{self.left_str} {self.operator} {self.right_str}'
        elif self.left and not self.left:
            return str(self.left)
        elif not self.left and self.right:
            return str(self.right)
        else:
            return ''

    @property
    @abstractmethod
    def operator(self) -> str:
        pass

    @property
    @abstractmethod
    def left_str(self) -> str:
        pass

    @property
    @abstractmethod
    def right_str(self) -> str:
        pass


class IntersectionOperationExpression(LogicalOperationExpression):

    @property
    def operator(self) -> str:
        return 'AND'

    @property
    def left_str(self) -> str:
        if isinstance(self.left, UnionOperationExpression):
            return f'({self.left})'
        else:
            return str(self.left)

    @property
    def right_str(self) -> str:
        if isinstance(self.right, UnionOperationExpression):
            return f'({self.right})'
        else:
            return str(self.right)


class UnionOperationExpression(LogicalOperationExpression):

    @property
    def operator(self) -> str:
        return 'OR'

    @property
    def left_str(self) -> str:
        if isinstance(self.left, IntersectionOperationExpression):
            return f'({self.left})'
        else:
            return str(self.left)

    @property
    def right_str(self) -> str:
        if isinstance(self.right, IntersectionOperationExpression):
            return f'({self.right})'
        else:
            return str(self.right)


class ClauseExpression(Expression):

    @abstractmethod
    def __str__(self) -> str:
        pass


class AsClauseExpression(ClauseExpression):

    def __init__(
            self,
            expression: Expression,
            alias: Expression,
    ) -> None:
        self.expression = expression
        self.alias = alias

    def __str__(self) -> str:
        return f'{self.expression} AS {self.alias}'


class AscClauseExpression(ClauseExpression):

    def __init__(
            self,
            expression: Expression,
            flag: bool | UndefinedExpression = True,
    ):
        self.expression = expression
        self.flag = flag

    def __str__(self) -> str:
        if self:
            if self.flag:
                return 'ASC'
            else:
                return 'DESC'
        else:
            return ''

    def __bool__(self) -> bool:
        return isinstance(self.flag, bool)


class DescClauseExpression(ClauseExpression):

    def __init__(
            self,
            expression: Expression,
            flag: bool | UndefinedExpression = True,
    ):
        self.expression = expression
        self.flag = flag

    def __str__(self) -> str:
        if self:
            if self.flag:
                return 'DESC'
            else:
                return 'ASC'
        else:
            return ''

    def __bool__(self) -> bool:
        return isinstance(self.flag, bool)


class IsClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} IS {self.right}'

    def __bool__(self) -> bool:
        return bool(self.left) or bool(self.right)


class IsNotClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ) -> None:
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} IS NOT {self.right}'

    def __bool__(self) -> bool:
        return bool(self.left) or bool(self.right)


class InClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: list[Expression],
    ) -> None:
        self.left = left
        self.right = right

    def __str__(self):
        if self:
            return f"{self.left} IN ({', '.join([str(expression) for expression in self.right])})"
        else:
            return ''


class NotInClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: list[Expression],
    ) -> None:
        self.left = left
        self.right = right

    def __str__(self):
        if self:
            return f"{self.left} NOT IN ({', '.join([str(expression) for expression in self.right])})"
        else:
            return ''


class BetweenClauseExpression(ClauseExpression):

    def __init__(
            self,
            expression: Expression,
            start: Expression,
            end: Expression,
    ) -> None:
        self.expression = expression
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f'{self.expression} BETWEEN {self.start} AND {self.end}'


class FilterClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} FILTER ({self.right})'


class JoinClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} JOIN {self.right}'


class LeftJoinClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} LEFT JOIN {self.right}'


class RightJoinClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} RIGHT JOIN {self.right}'


class InnerJoinClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} INNER JOIN {self.right}'


class FullJoinClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} FULL JOIN {self.right}'


class CrossJoinClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} CROSS JOIN {self.right}'


class OnClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} ON {self.right}'


class OverClauseExpression(ClauseExpression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
    ):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f'{self.left} OVER {self.right}'


class PrecedingClauseExpression(ClauseExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'{self.expression} PRECEDING'


class FollowingClauseExpression(ClauseExpression):

    def __init__(
            self,
            expression: Expression,
    ):
        self.expression = expression

    def __str__(self) -> str:
        return f'{self.expression} FOLLOWING'


class QueryExpression(Expression):

    def __init__(
            self,
            query: Query,
    ):
        self.query = query

    def __str__(self) -> str:
        return f'({self.query})'
