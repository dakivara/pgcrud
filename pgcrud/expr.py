from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from psycopg.sql import SQL, Identifier, Composed, Literal

from pgcrud.operators.filter import Between, FilterOperator, UndefinedFilter, Equal, NotEqual, GreaterThan, GreaterThanEqual, LessThan, LessThanEqual, IsNull, IsNotNull, IsIn, IsNotIn
from pgcrud.operators.sort import Ascending, Descending, UndefinedSort
from pgcrud.types import HowValueType
from pgcrud.undefined import Undefined
from pgcrud.utils import ensure_seq

if TYPE_CHECKING:
    from pgcrud.query import Query


__all__ = [
    'make_expr',
    'Expr',
    'UndefinedExpr',
    'ScalarExpr',
    'NullExpr',
    'LiteralExpr',
    'ReferenceExpr',
    'TableReferenceExpr',
    'ArithmeticExpr',
    'AddExpr',
    'SubExpr',
    'MulExpr',
    'TrueDivExpr',
    'PowExpr',
    'JoinExpr',
    'JoinOnExpr',
    'OverExpr',
    'AliasExpr',
    'QueryExpr',
    'FunExpr',
    'CountExpr',
    'SumExpr',
    'AvgExpr',
    'MinExpr',
    'MaxExpr',
    'ArrayAggExpr',
    'JsonAggExpr',
    'CoalesceExpr',
    'ToJsonExpr',
]


def make_expr(value: Any) -> 'Expr':
    if not isinstance(value, Expr):
        if value is None:
            value = NullExpr()
        elif value is Undefined:
            value = UndefinedExpr()
        else:
            value = LiteralExpr(value)
    return value


@dataclass
class Expr:

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    def get_inner_composed(self) -> Composed:
        return self.get_composed()

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return not isinstance(self, UndefinedExpr)

    def JOIN(self, expr: 'Expr') -> 'JoinExpr':
        return JoinExpr(self, expr)

    def INNER_JOIN(self, expr: 'Expr') -> 'JoinExpr':
        return JoinExpr(self, expr, 'INNER')

    def FULL_JOIN(self, expr: 'Expr') -> 'JoinExpr':
        return JoinExpr(self, expr, 'FULL')

    def LEFT_JOIN(self, expr: 'Expr') -> 'JoinExpr':
        return JoinExpr(self, expr, 'LEFT')

    def RIGHT_JOIN(self, expr: 'Expr') -> 'JoinExpr':
        return JoinExpr(self, expr, 'RIGHT')

    def CROSS_JOIN(self, expr: 'Expr') -> 'JoinExpr':
        return JoinExpr(self, expr, 'CROSS')

    def OVER(self, query: 'Query') -> 'OverExpr':
        return OverExpr(self, query)

    def AS(self, alias: 'str | Query') -> 'AliasExpr':
        return AliasExpr(self, alias)


@dataclass(repr=False, eq=False)
class ArithmeticExpr(Expr):

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    @abstractmethod
    def __add__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        pass

    def __radd__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        return make_expr(other) + self

    @abstractmethod
    def __sub__(self, other) -> 'SubExpr | UndefinedExpr':
        pass

    def __rsub__(self, other) -> 'SubExpr | UndefinedExpr':
        return make_expr(other) - self

    @abstractmethod
    def __mul__(self, other) -> 'MulExpr | UndefinedExpr':
        pass

    def __rmul__(self, other) -> 'MulExpr | UndefinedExpr':
        return make_expr(other) * self

    @abstractmethod
    def __truediv__(self, other) -> 'TrueDivExpr | UndefinedExpr':
        pass

    def __rtruediv__(self, other) -> 'TrueDivExpr | UndefinedExpr':
        return make_expr(other) / self

    @abstractmethod
    def __pow__(self, power) -> 'PowExpr | UndefinedExpr':
        pass

    def __rpow__(self, power) -> 'PowExpr | UndefinedExpr':
        return make_expr(power) ** self

    @abstractmethod
    def __eq__(self, other: Any) -> Equal | UndefinedFilter:  # type: ignore
        pass

    @abstractmethod
    def __ne__(self, other: Any) -> NotEqual | UndefinedFilter:   # type: ignore
        pass

    @abstractmethod
    def __gt__(self, other: Any) -> GreaterThan | UndefinedFilter:
        pass

    @abstractmethod
    def __ge__(self, other: Any) -> GreaterThanEqual | UndefinedFilter:
        pass

    @abstractmethod
    def __lt__(self, other: Any) -> LessThan | UndefinedFilter:
        pass

    @abstractmethod
    def __le__(self, other: Any) -> LessThanEqual | UndefinedFilter:
        pass

    @abstractmethod
    def IS_NULL(self, flag: bool | type[Undefined] = True) -> IsNull | UndefinedFilter:
        pass

    @abstractmethod
    def IS_NOT_NULL(self, flag: bool | type[Undefined] = True) -> IsNotNull | UndefinedFilter:
        pass

    @abstractmethod
    def IN(self, value: Any) -> IsIn | UndefinedFilter:
        pass

    @abstractmethod
    def NOT_IN(self, value: Any) -> IsNotIn | UndefinedFilter:
        pass

    @abstractmethod
    def BETWEEN(self, start: Any, end: Any) -> Between | UndefinedFilter:
        pass

    @abstractmethod
    def ASC(self, flag: bool | type[Undefined] = True) -> Ascending | UndefinedSort:
        pass

    @abstractmethod
    def DESC(self, flag: bool | type[Undefined] = True) -> Descending | UndefinedSort:
        pass


@dataclass(repr=False, eq=False)
class UndefinedExpr(ArithmeticExpr):

    def get_composed(self) -> Composed:
        return Composed([])

    def __add__(self, other: Any) -> 'UndefinedExpr':
        return UndefinedExpr()

    def __sub__(self, other) -> 'UndefinedExpr':
        return UndefinedExpr()

    def __mul__(self, other) -> 'UndefinedExpr':
        return UndefinedExpr()

    def __truediv__(self, other) -> 'UndefinedExpr':
        return UndefinedExpr()

    def __pow__(self, power) -> 'UndefinedExpr':
        return UndefinedExpr()

    def __eq__(self, other: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def __ne__(self, other: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def __gt__(self, other: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def __ge__(self, other: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def __lt__(self, other: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def __le__(self, other: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def IS_NULL(self, flag: bool | type[Undefined] = True) -> UndefinedFilter:
        return UndefinedFilter()

    def IS_NOT_NULL(self, flag: bool | type[Undefined] = True) -> UndefinedFilter:
        return UndefinedFilter()

    def IN(self, value: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def NOT_IN(self, value: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def BETWEEN(self, start: Any, end: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def ASC(self, flag: bool | type[Undefined] = True) -> UndefinedSort:
        return UndefinedSort()

    def DESC(self, flag: bool | type[Undefined] = True) -> UndefinedSort:
        return UndefinedSort()


@dataclass(repr=False, eq=False)
class DefinedExpr(ArithmeticExpr):

    @abstractmethod
    def __add__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        pass

    @abstractmethod
    def __sub__(self, other) -> 'SubExpr | UndefinedExpr':
        pass

    @abstractmethod
    def __mul__(self, other) -> 'MulExpr | UndefinedExpr':
        pass

    @abstractmethod
    def __truediv__(self, other) -> 'TrueDivExpr | UndefinedExpr':
        pass

    @abstractmethod
    def __pow__(self, power) -> 'PowExpr | UndefinedExpr':
        pass

    def __eq__(self, other: Any) -> Equal | UndefinedFilter:  # type: ignore
        return Equal(self, expr) if (expr := make_expr(other)) else UndefinedFilter()

    def __ne__(self, other: Any) -> NotEqual | UndefinedFilter:   # type: ignore
        return NotEqual(self, expr) if (expr := make_expr(other)) else UndefinedFilter()

    def __gt__(self, other: Any) -> GreaterThan | UndefinedFilter:
        return GreaterThan(self, expr) if (expr := make_expr(other)) else UndefinedFilter()

    def __ge__(self, other: Any) -> GreaterThanEqual | UndefinedFilter:
        return GreaterThanEqual(self, expr) if (expr := make_expr(other)) else UndefinedFilter()

    def __lt__(self, other: Any) -> LessThan | UndefinedFilter:
        return LessThan(self, expr) if (expr := make_expr(other)) else UndefinedFilter()

    def __le__(self, other: Any) -> LessThanEqual | UndefinedFilter:
        return LessThanEqual(self, expr) if (expr := make_expr(other)) else UndefinedFilter()

    def IS_NULL(self, flag: bool | type[Undefined] = True) -> IsNull | UndefinedFilter:
        return IsNull(self, flag) if isinstance(flag, bool) else UndefinedFilter()

    def IS_NOT_NULL(self, flag: bool | type[Undefined] = True) -> IsNotNull | UndefinedFilter:
        return IsNotNull(self, flag) if isinstance(flag, bool) else UndefinedFilter()

    def IN(self, value: Any) -> IsIn | UndefinedFilter:
        if value is Undefined:
            return UndefinedFilter()
        else:
            exprs = []
            for v in ensure_seq(value):
                if expr := make_expr(v):
                    exprs.append(expr)
            return IsIn(self, exprs)

    def NOT_IN(self, value: Any) -> IsNotIn | UndefinedFilter:
        if value is Undefined:
            return UndefinedFilter()
        else:
            exprs = []
            for v in ensure_seq(value):
                if expr := make_expr(v):
                    exprs.append(expr)
            return IsNotIn(self, exprs)

    def BETWEEN(self, start: Any, end: Any) -> Between | UndefinedFilter:
        start_expr = make_expr(start)
        end_expr = make_expr(end)
        return Between(self, start_expr, end_expr) if start_expr and end_expr else UndefinedFilter()

    def ASC(self, flag: bool | type[Undefined] = True) -> Ascending | UndefinedSort:
        return Ascending(self, flag) if isinstance(flag, bool) else UndefinedSort()

    def DESC(self, flag: bool | type[Undefined] = True) -> Descending | UndefinedSort:
        return Descending(self, flag) if isinstance(flag, bool) else UndefinedSort()


@dataclass(repr=False, eq=False)
class ScalarExpr(DefinedExpr):

    @abstractmethod
    def get_composed(self) -> Composed:
        pass
        
    def __add__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, AddExpr):
            return AddExpr([self] + other.exprs)
        elif isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return AddExpr([self, other])

    def __sub__(self, other: Any) -> 'SubExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, SubExpr):
            return SubExpr([self] + other.exprs)
        elif isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return SubExpr([self, other])

    def __mul__(self, other: Any) -> 'MulExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, MulExpr):
            return MulExpr([self] + other.exprs)
        elif isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return MulExpr([self, other])

    def __truediv__(self, other: Any) -> 'TrueDivExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, TrueDivExpr):
            return TrueDivExpr([self] + other.exprs)
        elif isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return TrueDivExpr([self, other])

    def __pow__(self, power) -> 'PowExpr | UndefinedExpr':
        power = make_expr(power)
        if isinstance(power, PowExpr):
            return PowExpr([self] + power.exprs)
        elif isinstance(power, UndefinedExpr):
            return UndefinedExpr()
        else:
            return PowExpr([self, power])


@dataclass(repr=False, eq=False)
class NullExpr(ScalarExpr):

    def get_composed(self) -> Composed:
        return Composed([SQL('NULL')])


@dataclass(repr=False, eq=False)
class LiteralExpr(ScalarExpr):
    value: Any

    def get_composed(self) -> Composed:
        if hasattr(self.value, 'get_composed'):
            return self.value.get_composed()
        else:
            return SQL('{}').format(Literal(self.value))


@dataclass(repr=False, eq=False)
class ReferenceExpr(ScalarExpr):
    _name: str
    _parent: 'ReferenceExpr | None' = None

    def __getattr__(self, name: str) -> 'ReferenceExpr':
        return ReferenceExpr(name, self)

    def __getitem__(self, item: 'ReferenceExpr | tuple[ReferenceExpr, ...]') -> 'TableReferenceExpr':
        return TableReferenceExpr(self, item if isinstance(item, tuple) else (item,))

    def __call__(self, name: str) -> 'ReferenceExpr':
        return ReferenceExpr(name, self)

    def get_composed(self) -> Composed:
        if self._parent:
            return SQL('{}.{}').format(self._parent.get_composed(), Identifier(self._name))
        else:
            return SQL('{}').format(Identifier(self._name))


@dataclass(repr=False, eq=False)
class TableReferenceExpr(Expr):
    expr: ReferenceExpr
    children: tuple[ReferenceExpr, ...]

    def get_composed(self) -> Composed:
        return SQL('{} ({})').format(self.expr.get_composed(), SQL(', ').join([expr.get_composed() for expr in self.children]))


@dataclass(repr=False, eq=False)
class CompositeExpr(DefinedExpr):
    exprs: list[Expr]

    @property
    @abstractmethod
    def operator(self) -> SQL:
        pass

    def get_composed(self) -> Composed:
        return self.operator.join([expr.get_inner_composed() for expr in self.exprs])

    def get_inner_composed(self) -> Composed:
        if len(self.get_composed()._obj) > 1:
            return Composed([SQL('('), self.get_composed(), SQL(')')])
        else:
            return self.get_composed()


@dataclass(repr=False, eq=False)
class AddExpr(CompositeExpr):

    @property
    def operator(self) -> SQL:
        return SQL(' + ')

    def __add__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, AddExpr):
            return AddExpr(self.exprs + other.exprs)
        elif isinstance(other, CompositeExpr):
            return AddExpr([self, other])
        elif isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return AddExpr(self.exprs + [other])

    def __sub__(self, other: Any) -> 'SubExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return SubExpr([self, other])

    def __mul__(self, other: Any) -> 'MulExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return MulExpr([self, make_expr(other)])

    def __truediv__(self, other: Any) -> 'TrueDivExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return TrueDivExpr([self, other])

    def __pow__(self, power: Any) -> 'PowExpr | UndefinedExpr':
        power = make_expr(power)
        if isinstance(power, UndefinedExpr):
            return UndefinedExpr()
        else:
            return PowExpr([self, power])


@dataclass(repr=False, eq=False)
class SubExpr(CompositeExpr):

    @property
    def operator(self) -> SQL:
        return SQL(' - ')

    def __add__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return AddExpr([self, other])

    def __sub__(self, other: Any) -> 'SubExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, SubExpr):
            return SubExpr(self.exprs + other.exprs)
        elif isinstance(other, CompositeExpr):
            return SubExpr([self, other])
        elif isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return SubExpr(self.exprs + [other])

    def __mul__(self, other: Any) -> 'MulExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return MulExpr([self, other])

    def __truediv__(self, other: Any) -> 'TrueDivExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return TrueDivExpr([self, other])

    def __pow__(self, power: Any) -> 'PowExpr | UndefinedExpr':
        power = make_expr(power)
        if isinstance(power, UndefinedExpr):
            return UndefinedExpr()
        else:
            return PowExpr([self, power])


@dataclass(repr=False, eq=False)
class MulExpr(CompositeExpr):

    @property
    def operator(self) -> SQL:
        return SQL(' * ')

    def __add__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return AddExpr([self, other])

    def __sub__(self, other: Any) -> 'SubExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return SubExpr([self, other])

    def __mul__(self, other: Any) -> 'MulExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, MulExpr):
            return MulExpr(self.exprs + other.exprs)
        elif isinstance(other, CompositeExpr):
            return MulExpr([self, other])
        elif isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return MulExpr(self.exprs + [other])

    def __truediv__(self, other: Any) -> 'TrueDivExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return TrueDivExpr([self, other])

    def __pow__(self, power: Any) -> 'PowExpr | UndefinedExpr':
        power = make_expr(power)
        if isinstance(power, UndefinedExpr):
            return UndefinedExpr()
        else:
            return PowExpr([self, power])


@dataclass(repr=False, eq=False)
class TrueDivExpr(CompositeExpr):

    @property
    def operator(self) -> SQL:
        return SQL(' / ')

    def __add__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return AddExpr([self, other])

    def __sub__(self, other: Any) -> 'SubExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return SubExpr([self, other])

    def __mul__(self, other: Any) -> 'MulExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return MulExpr([self, other])

    def __truediv__(self, other: Any) -> 'TrueDivExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, TrueDivExpr):
            return TrueDivExpr(self.exprs + other.exprs)
        elif isinstance(other, CompositeExpr):
            return TrueDivExpr([self, other])
        elif isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return TrueDivExpr(self.exprs + [other])

    def __pow__(self, power: Any) -> 'PowExpr | UndefinedExpr':
        power = make_expr(power)
        if isinstance(power, UndefinedExpr):
            return UndefinedExpr()
        else:
            return PowExpr([self, power])


@dataclass(repr=False, eq=False)
class PowExpr(CompositeExpr):

    @property
    def operator(self) -> SQL:
        return SQL(' ^ ')

    def __add__(self, other: Any) -> 'AddExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return AddExpr([self, other])

    def __sub__(self, other: Any) -> 'SubExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return SubExpr([self, other])

    def __mul__(self, other: Any) -> 'MulExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return MulExpr([self, other])

    def __truediv__(self, other: Any) -> 'TrueDivExpr | UndefinedExpr':
        other = make_expr(other)
        if isinstance(other, UndefinedExpr):
            return UndefinedExpr()
        else:
            return TrueDivExpr([self, other])

    def __pow__(self, power: Any) -> 'PowExpr | UndefinedExpr':
        power = make_expr(power)
        if isinstance(power, PowExpr):
            return PowExpr(self.exprs + power.exprs)
        elif isinstance(power, CompositeExpr):
            return PowExpr([self, power])
        elif isinstance(power, UndefinedExpr):
            return UndefinedExpr()
        else:
            return PowExpr(self.exprs + [power])


@dataclass(repr=False, eq=False)
class JoinExpr(Expr):
    expr: Expr
    joined_expr: Expr
    how: HowValueType | None = None

    @property
    def join_type(self) -> Composed:
        if self.how:
            return SQL('{} JOIN').format(SQL(self.how))
        else:
            return Composed([SQL('JOIN')])

    def get_composed(self) -> Composed:
        return SQL('{} {} {}').format(self.expr.get_composed(), self.join_type, self.joined_expr.get_composed())

    def ON(self, on: FilterOperator) -> 'JoinOnExpr':
        return JoinOnExpr(self, on)


@dataclass(repr=False, eq=False)
class JoinOnExpr(Expr):
    expr: JoinExpr
    on: FilterOperator

    def get_composed(self) -> Composed:
        return SQL('{} ON {}').format(self.expr.get_composed(), self.on.get_composed())


@dataclass(repr=False, eq=False)
class OverExpr(Expr):
    expr: Expr
    query: 'Query'

    def get_composed(self) -> Composed:
        return SQL('{} OVER ({})').format(self.expr.get_composed(), self.query.get_composed())


@dataclass(repr=False, eq=False)
class AliasExpr(Expr):
    expr: Expr
    alias: 'str | Query'

    def get_composed(self) -> Composed:
        if isinstance(self.alias, str):
            return SQL('{} AS {}').format(self.expr.get_composed(), Identifier(self.alias))
        else:
            return SQL('{} AS ({})').format(self.expr.get_composed(), self.alias.get_composed())


@dataclass(repr=False, eq=False)
class QueryExpr(Expr):
    query: 'Query'
    alias: str

    @abstractmethod
    def get_composed(self) -> Composed:
        return SQL('({}) AS {}').format(self.query.get_composed(), Identifier(self.alias))


@dataclass(repr=False, eq=False)
class FunExpr(ScalarExpr):

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


@dataclass(repr=False, eq=False)
class CountExpr(FunExpr):
    expr: Expr

    def get_composed(self) -> Composed:
        return SQL('count({})').format(self.expr.get_composed())


@dataclass(repr=False, eq=False)
class SumExpr(FunExpr):
    expr: Expr

    def get_composed(self) -> Composed:
        return SQL('sum({})').format(self.expr.get_composed())


@dataclass(repr=False, eq=False)
class AvgExpr(FunExpr):
    expr: Expr

    def get_composed(self) -> Composed:
        return SQL('avg({})').format(self.expr.get_composed())


@dataclass(repr=False, eq=False)
class MinExpr(FunExpr):
    expr: Expr

    def get_composed(self) -> Composed:
        return SQL('min({})').format(self.expr.get_composed())


@dataclass(repr=False, eq=False)
class MaxExpr(FunExpr):
    expr: Expr

    def get_composed(self) -> Composed:
        return SQL('max({})').format(self.expr.get_composed())


@dataclass(repr=False, eq=False)
class ArrayAggExpr(FunExpr):
    expr: Expr

    def get_composed(self) -> Composed:
        return SQL('array_agg({})').format(self.expr.get_composed())


@dataclass(repr=False, eq=False)
class JsonAggExpr(FunExpr):
    expr: Expr

    def get_composed(self) -> Composed:
        return SQL('json_agg({})').format(self.expr.get_composed())


@dataclass(repr=False, eq=False)
class CoalesceExpr(FunExpr):
    exprs: Sequence[Expr]

    def get_composed(self) -> Composed:
        return SQL('coalesce({})').format(SQL(', ').join([expr.get_inner_composed() for expr in self.exprs]))


@dataclass(repr=False, eq=False)
class ToJsonExpr(FunExpr):
    expr: Expr

    def get_composed(self) -> Composed:
        return SQL('to_json({})').format(self.expr.get_composed())
