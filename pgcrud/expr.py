from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from psycopg.sql import SQL, Identifier, Composed, Literal

from pgcrud.operators import FilterOperator, JoinOn
from pgcrud.operators.filter import UndefinedFilter, Equal, NotEqual, GreaterThan, GreaterThanEqual, LessThan, LessThanEqual, IsNull, IsNotNull, IsIn, IsNotIn
from pgcrud.operators.join import CrossJoin, InnerJoin, JoinOperator, Join, RightJoin, LeftJoin, FullJoin
from pgcrud.operators.sort import Ascending, Descending, UndefinedSort
from pgcrud.query import Query
from pgcrud.types import HowValueType
from pgcrud.undefined import Undefined


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
    'AliasExpr',
    'QueryExpr',
    'FunExpr',
    'SumExpr',
    'AvgExpr',
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

    @abstractmethod
    def get_inner_composed(self) -> Composed:
        pass

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return str(self)

    def __bool__(self):
        return not isinstance(self, UndefinedExpr)

    def JOIN(self, expr: 'Expr', on: FilterOperator) -> 'JoinExpr | UndefinedExpr':
        if isinstance(self, UndefinedExpr):
            return UndefinedExpr()
        else:
            return JoinExpr(self, Join(expr, on))

    def INNER_JOIN(self, expr: 'Expr', on: FilterOperator) -> 'JoinExpr | UndefinedExpr':
        if isinstance(self, UndefinedExpr):
            return UndefinedExpr()
        else:
            return JoinExpr(self, InnerJoin(expr, on))

    def FULL_JOIN(self, expr: 'Expr', on: FilterOperator) -> 'JoinExpr | UndefinedExpr':
        if isinstance(self, UndefinedExpr):
            return UndefinedExpr()
        else:
            return JoinExpr(self, FullJoin(expr, on))

    def LEFT_JOIN(self, expr: 'Expr', on: FilterOperator) -> 'JoinExpr | UndefinedExpr':
        if isinstance(self, UndefinedExpr):
            return UndefinedExpr()
        else:
            return JoinExpr(self, LeftJoin(expr, on))

    def RIGHT_JOIN(self, expr: 'Expr', on: FilterOperator) -> 'JoinExpr | UndefinedExpr':
        if isinstance(self, UndefinedExpr):
            return UndefinedExpr()
        else:
            return JoinExpr(self, RightJoin(expr, on))

    def CROSS_JOIN(self, expr: 'Expr') -> 'JoinExpr | UndefinedExpr':
        if isinstance(self, UndefinedExpr):
            return UndefinedExpr()
        else:
            return JoinExpr(self, CrossJoin(expr))


@dataclass(repr=False, eq=False)
class ArithmeticExpr(Expr):

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    @abstractmethod
    def get_inner_composed(self) -> Composed:
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
    def IN(self, values: Any) -> IsIn | UndefinedFilter:
        pass

    @abstractmethod
    def NOT_IN(self, values: Any) -> IsNotIn | UndefinedFilter:
        pass

    @abstractmethod
    def ASC(self, flag: bool | type[Undefined] = True) -> Ascending | UndefinedSort:
        pass

    @abstractmethod
    def DESC(self, flag: bool | type[Undefined] = True) -> Descending | UndefinedSort:
        pass

    def OVER(self):
        pass

    def AS(self, alias: str) -> 'AliasExpr':
        return AliasExpr(self, alias)


@dataclass(repr=False, eq=False)
class UndefinedExpr(ArithmeticExpr):

    def get_composed(self) -> Composed:
        return Composed([])

    def get_inner_composed(self) -> Composed:
        return self.get_composed()

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

    def IN(self, values: Any) -> UndefinedFilter:
        return UndefinedFilter()

    def NOT_IN(self, values: Any) -> UndefinedFilter:
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

    def IN(self, values: list[Any]) -> IsIn | UndefinedFilter:
        return IsIn(self, make_expr([value for value in values if value is not Undefined]))

    def NOT_IN(self, values: list[Any]) -> IsNotIn | UndefinedFilter:
        return IsNotIn(self, make_expr([value for value in values if value is not Undefined]))

    def ASC(self, flag: bool | type[Undefined] = True) -> Ascending | UndefinedSort:
        return Ascending(self, flag) if isinstance(flag, bool) else UndefinedSort()

    def DESC(self, flag: bool | type[Undefined] = True) -> Descending | UndefinedSort:
        return Descending(self, flag) if isinstance(flag, bool) else UndefinedSort()


@dataclass(repr=False, eq=False)
class ScalarExpr(DefinedExpr):

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    def get_inner_composed(self) -> Composed:
        return self.get_composed()
        
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
        return SQL('{}').format(Literal(self.value))


@dataclass(repr=False, eq=False)
class ReferenceExpr(ScalarExpr):
    _name: str
    _parent: 'ReferenceExpr | None' = None

    def __getattr__(self, name: str) -> 'ReferenceExpr':
        if name in ['__get_pydantic_core_schema__', '__get_pydantic_json_schema__', '__modify_schema__', '__origin__']:
            return super().__getattribute__(name)
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

    def get_inner_composed(self) -> Composed:
        return self.get_composed()


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
    operator: JoinOperator

    def get_composed(self) -> Composed:
        if self.operator:
            return SQL('{} {}').format(self.expr.get_composed(), self.operator.get_composed())
        else:
            return self.expr.get_composed()

    def get_inner_composed(self) -> Composed:
        return self.get_composed()


@dataclass(repr=False, eq=False)
class AliasExpr(Expr):
    expr: Expr
    alias: str

    def get_composed(self) -> Composed:
        return SQL('{} AS {}').format(self.expr.get_composed(), Identifier(self.alias))


@dataclass(repr=False, eq=False)
class QueryExpr(Expr):
    query: Query
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
