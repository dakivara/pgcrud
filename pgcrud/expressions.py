from __future__ import annotations

from abc import abstractmethod
from typing import Any, Literal as LiteralType, Self, TYPE_CHECKING, Sequence

from psycopg.sql import Literal as _Literal, Identifier as _Identifier

from pgcrud.clauses import (
    Clause,
    As,
    Asc,
    Filter,
    Join,
    On,
    Where,
    RightJoin,
    LeftJoin,
    CrossJoin,
    FullJoin,
    InnerJoin,
    Desc,
    Following,
    Preceding,
    Over,
)
from pgcrud.filter_conditions import (
    Equal,
    NotEqual,
    GreatThan,
    GreaterThanEqual,
    LessThan,
    LessThanEqual,
    FilterCondition,
    Between,
    IsNull,
    IsNotNull,
    In,
    NotIn,
)
from pgcrud.utils import ensure_seq

if TYPE_CHECKING:
    from pgcrud.query import Query


__all__ = [
    'make_expr',
    'Expression',
    'Undefined',
    'Unbounded',
    'CurrentRow',
    'Excluded',
    'Star',
    'Literal',
    'Placeholder',
    'Identifier',
    'TableIdentifier',
    'ComposedExpression',
    'Addition',
    'Subtraction',
    'Multiplication',
    'Division',
    'Power',
    'DerivedTable',
    'Function',
    'RowNumber',
    'Count',
    'Sum',
    'Avg',
    'Min',
    'Max',
    'ArrayAgg',
    'JsonAgg',
    'Coalesce',
    'ToJson',

    'Crypt',
    'GenSalt',
]


def make_expr(value: Any) -> Expression:
    if getattr(value, '_tag', '') == 'QUERY':
        return DerivedTable(value)
    elif getattr(value, '_tag', '') == 'EXPRESSION':
        return value
    else:
        return Literal(value)


class Expression:

    _tag = 'EXPRESSION'

    def __init__(
            self,
            clauses: list[Clause] | None = None,
    ) -> None:
        self._clauses = clauses or []

    def __str__(self) -> str:
        if self:
            return ' '.join([self._base_str] + [str(clause) for clause in self._clauses])
        else:
            return ''

    def __bool__(self) -> bool:
        return all(self._clauses)

    def __repr__(self):
        return str(self)

    def __add__(self, other: Any) -> Addition:
        return Addition(self, make_expr(other))

    def __radd__(self, other: Any) -> Addition:
        return Literal(other) + self

    def __sub__(self, other: Any) -> Subtraction:
        return Subtraction(self, make_expr(other))

    def __rsub__(self, other: Any) -> Subtraction:
        return Literal(other) - self

    def __mul__(self, other: Any) -> Multiplication:
        return Multiplication(self, make_expr(other))

    def __rmul__(self, other: Any) -> Multiplication:
        return Literal(other) * self

    def __truediv__(self, other: Any) -> Division:
        return Division(self, make_expr(other))

    def __rtruediv__(self, other: Any) -> Division:
        return Literal(other) / self

    def __pow__(self, other: Any) -> Power:
        return Power(self, make_expr(other))

    def __rpow__(self, other: Any) -> Power:
        return Literal(other) ** self

    def __eq__(self, other: Any) -> Equal:  # type: ignore
        return Equal(self, make_expr(other))

    def __ne__(self, other: Any) -> NotEqual:  # type: ignore
        return NotEqual(self, make_expr(other))

    def __gt__(self, other: Any) -> GreatThan:
        return GreatThan(self, make_expr(other))

    def __ge__(self, other: Any) -> GreaterThanEqual:
        return GreaterThanEqual(self, make_expr(other))

    def __lt__(self, other: Any) -> LessThan:
        return LessThan(self, make_expr(other))

    def __le__(self, other: Any) -> LessThanEqual:
        return LessThanEqual(self, make_expr(other))

    @property
    @abstractmethod
    def _base_str(self) -> str:
        pass

    def AS(self, alias: Expression | Query) -> Self:
        self._clauses.append(As(make_expr(alias)))
        return self

    def ASC(self, flag: bool | Undefined = True) -> Self:
        self._clauses.append(Asc(flag))
        return self

    def BETWEEN(self, start: Any, end: Any) -> Between:
        return Between(self, make_expr(start), make_expr(end))

    def CROSS_JOIN(self, expression: Expression) -> Self:
        self._clauses.append(CrossJoin(expression))
        return self

    def DESC(self, flag: bool | Undefined = True) -> Self:
        self._clauses.append(Desc(flag))
        return self

    def FILTER(self, where: Where) -> Self:
        self._clauses.append(Filter(where))
        return self

    @property
    def FOLLOWING(self) -> Self:
        self._clauses.append(Following())
        return self

    def FULL_JOIN(self, expression: Expression) -> Self:
        self._clauses.append(FullJoin(expression))
        return self

    def IN(self, *args: Any) -> In:
        return In(self, [make_expr(arg) for arg in args])

    def INNER_JOIN(self, expression: Expression) -> Self:
        self._clauses.append(InnerJoin(expression))
        return self

    def IS_NOT_NULL(self, flag: bool | Undefined = True) -> IsNotNull:
        return IsNotNull(self, flag)

    def IS_NULL(self, flag: bool | Undefined = True) -> IsNull:
        return IsNull(self, flag)

    def JOIN(self, expression: Expression) -> Self:
        self._clauses.append(Join(expression))
        return self

    def LEFT_JOIN(self, expression: Expression) -> Self:
        self._clauses.append(LeftJoin(expression))
        return self

    def NOT_IN(self, *args: Any) -> NotIn:
        return NotIn(self, [make_expr(arg) for arg in args])

    def ON(self, condition: FilterCondition) -> Self:
        self._clauses.append(On(condition))
        return self

    def OVER(self, query: Query) -> Self:
        self._clauses.append(Over(DerivedTable(query)))
        return self

    @property
    def PRECEDING(self) -> Self:
        self._clauses.append(Preceding())
        return self

    def RIGHT_JOIN(self, expression: Expression) -> Self:
        self._clauses.append(RightJoin(expression))
        return self


class Undefined(Expression):

    def __bool__(self) -> bool:
        return False

    @property
    def _base_str(self) -> str:
        return ''

    @property
    def _clauses(self) -> list[Clause]:
        return []

    @_clauses.setter
    def _clauses(self, clauses: list[Clause]) -> None:
        pass


class Unbounded(Expression):

    @property
    def _base_str(self) -> str:
        return 'UNBOUNDED'


class CurrentRow(Expression):

    @property
    def _base_str(self) -> str:
        return 'CURRENT ROW'


class Excluded(Expression):

    @property
    def _base_str(self) -> str:
        return 'EXCLUDED'

    def __call__(self, item: str) -> Identifier:
        return Identifier(item, self)

    def __getattr__(self, item: str) -> Identifier:
        return Identifier(item, self)


class Star(Expression):

    def __init__(
            self,
            identifier: Identifier | None = None,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.identifier = identifier

    @property
    def _base_str(self) -> str:
        if self.identifier:
            return f'{self.identifier}.*'
        else:
            return '*'


class Literal(Expression):

    def __init__(
            self,
            value: Any,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self._value = value

    @property
    def _base_str(self) -> str:
        return _Literal(self._value).as_string()


class Placeholder(Expression):

    def __init__(
            self,
            name: str | None = None,
            clauses: list[Clause] | None = None,
    ) -> None:
        super().__init__(clauses)
        self._name = name

    @property
    def _base_str(self) -> str:
        if self._name:
            return f'%({self._name})s'
        else:
            return '%s'


class IdentifierType(type):

    def __getattr__(cls, item) -> Identifier:
        return cls(item)


class Identifier(Expression, metaclass=IdentifierType):

    def __init__(
            self,
            name: str,
            parent: Identifier | Excluded | None = None,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self._name = name
        self._parent = parent

    def __call__(self, item: str) -> Identifier:
        return Identifier(item, self)

    def __getattr__(self, item: str) -> Identifier:
        return Identifier(item, self)

    def __getitem__(self, item: Identifier | tuple[Identifier, ...]) -> TableIdentifier:
        return TableIdentifier(self, ensure_seq(item))

    @property
    def _base_str(self) -> str:
        if self._parent:
            return f'{self._parent}.{_Identifier(self._name).as_string()}'
        else:
            return _Identifier(self._name).as_string()

    @property
    def STAR(self) -> Star:
        return Star(self)


class TableIdentifier(Expression):

    def __init__(
            self,
            identifier: Identifier,
            columns: Sequence[Identifier],
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self._identifier = identifier
        self._columns = columns

    @property
    def _base_str(self) -> str:
        return f"{self._identifier} ({', '.join([str(column) for column in self._columns])})"


class ComposedExpression(Expression):

    def __init__(
            self,
            left: Expression,
            right: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self._left = left
        self._right = right

    @property
    def _base_str(self) -> str:
        return f'{self._left_str} {self._operator} {self._right_str}'

    @property
    @abstractmethod
    def _operator(self) -> str:
        pass

    @property
    @abstractmethod
    def _left_str(self) -> str:
        pass

    @property
    @abstractmethod
    def _right_str(self) -> str:
        pass


class Addition(ComposedExpression):

    @property
    def _operator(self) -> str:
        return '+'

    @property
    def _left_str(self) -> str:
        if isinstance(self._left, (Subtraction, Multiplication, Division, Power)):
            return f'({self._left})'
        else:
            return str(self._left)

    @property
    def _right_str(self) -> str:
        if isinstance(self._right, (Subtraction, Multiplication, Division, Power)):
            return f'({self._right})'
        else:
            return str(self._right)


class Subtraction(ComposedExpression):

    @property
    def _operator(self) -> str:
        return '-'

    @property
    def _left_str(self) -> str:
        if isinstance(self._left, (Addition, Multiplication, Division, Power)):
            return f'({self._left})'
        else:
            return str(self._left)

    @property
    def _right_str(self) -> str:
        if isinstance(self._right, ComposedExpression):
            return f'({self._right})'
        else:
            return str(self._right)


class Multiplication(ComposedExpression):

    @property
    def _operator(self) -> str:
        return '*'

    @property
    def _left_str(self) -> str:
        if isinstance(self._left, (Addition, Subtraction, Division, Power)):
            return f'({self._left})'
        else:
            return str(self._left)

    @property
    def _right_str(self) -> str:
        if isinstance(self._right, (Addition, Subtraction, Division, Power)):
            return f'({self._right})'
        else:
            return str(self._right)


class Division(ComposedExpression):

    @property
    def _operator(self) -> str:
        return '/'

    @property
    def _left_str(self) -> str:
        if isinstance(self._left, (Addition, Subtraction, Multiplication, Power)):
            return f'({self._left})'
        else:
            return str(self._left)

    @property
    def _right_str(self) -> str:
        if isinstance(self._right, ComposedExpression):
            return f'({self._right})'
        else:
            return str(self._right)


class Power(ComposedExpression):

    @property
    def _operator(self) -> str:
        return '^'

    @property
    def _left_str(self) -> str:
        if isinstance(self._left, ComposedExpression):
            return f'({self._left})'
        else:
            return str(self._left)

    @property
    def _right_str(self) -> str:
        if isinstance(self._right, (Addition, Subtraction, Multiplication, Division)):
            return f'({self._right})'
        else:
            return str(self._right)


class DerivedTable(Expression):

    def __init__(
            self,
            query: Query,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self._query = query

    @property
    def _base_str(self) -> str:
        return f'({self._query})'


class Function(Expression):

    @property
    @abstractmethod
    def _base_str(self) -> str:
        pass


class RowNumber(Function):

    @property
    def _base_str(self) -> str:
        return 'row_number()'


class Count(Function):

    def __init__(
            self,
            expression: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expression = expression

    @property
    def _base_str(self) -> str:
        return f'count({self.expression})'


class Sum(Function):

    def __init__(
            self,
            expression: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expression = expression

    @property
    def _base_str(self) -> str:
        return f'sum({self.expression})'


class Avg(Function):

    def __init__(
            self,
            expression: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expression = expression

    @property
    def _base_str(self) -> str:
        return f'avg({self.expression})'


class Min(Function):

    def __init__(
            self,
            expression: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expression = expression

    @property
    def _base_str(self) -> str:
        return f'min({self.expression})'


class Max(Function):

    def __init__(
            self,
            expression: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expression = expression

    @property
    def _base_str(self) -> str:
        return f'max({self.expression})'


class ArrayAgg(Function):

    def __init__(
            self,
            expression: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expression = expression

    @property
    def _base_str(self) -> str:
        return f'array_agg({self.expression})'


class JsonAgg(Function):

    def __init__(
            self,
            expression: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expression = expression

    @property
    def _base_str(self) -> str:
        return f'json_agg({self.expression})'


class Coalesce(Function):

    def __init__(
            self,
            expressions: Sequence[Expression],
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expressions = expressions

    @property
    def _base_str(self) -> str:
        return f"coalesce({', '.join([str(expression) for expression in self.expressions])})"


class ToJson(Function):

    def __init__(
            self,
            expression: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.expression = expression

    @property
    def _base_str(self) -> str:
        return f'to_json({self.expression})'


# pgcrypto


class Crypt(Function):

    def __init__(
            self,
            password: str,
            salt: Expression,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.password = _Literal(password).as_string()
        self.salt = salt

    @property
    def _base_str(self) -> str:
        return f'crypt({self.password}, {self.salt})'


class GenSalt(Function):

    def __init__(
            self,
            algorithm: LiteralType['bf', 'md5', 'sha256'],
            cost: int | None = None,
            clauses: list[Clause] | None = None,
    ):
        super().__init__(clauses)
        self.algorithm = _Literal(algorithm).as_string()
        self.cost = _Literal(cost).as_string() if cost else None

    @property
    def _base_str(self) -> str:
        if self.cost:
            return f'gen_salt({self.algorithm}, {self.cost})'
        else:
            return f'gen_salt({self.algorithm})'
