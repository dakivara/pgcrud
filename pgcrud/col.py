from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from psycopg.sql import SQL, Identifier, Composed, Literal

from pgcrud.operators.filter import Equal, NotEqual, GreaterThan, GreaterThanEqual, LessThan, LessThanEqual, IsNull, IsNotNull, IsIn, IsNotIn
from pgcrud.operators.sort import Ascending, Descending
from pgcrud.undefined import Undefined

if TYPE_CHECKING:
    from pgcrud.tab import Tab


__all__ = [
    'make_col',
    'Col',
    'UndefinedCol',
    'SimpleCol',
    'NullCol',
    'LiteralCol',
    'SingleCol',
    'ArithmeticCol',
    'AddCol',
    'SubCol',
    'MulCol',
    'TrueDivCol',
    'PowCol',
    'AliasCol',
    'FunCol',
    'SumCol',
    'AvgCol',
    'ToJsonCol',
    'JsonAggCol',
]


def make_col(value: Any) -> 'Col':
    if not isinstance(value, Col):
        if value is None:
            value = NullCol()
        elif value is Undefined:
            value = UndefinedCol()
        else:
            value = LiteralCol(value)
    return value


@dataclass
class Col:

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    @abstractmethod
    def get_inner_composed(self) -> Composed:
        pass

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return not isinstance(self, UndefinedCol)

    def __eq__(self, other: Any) -> Equal:  # type: ignore
        return Equal(self, make_col(other))

    def __ne__(self, other: Any) -> NotEqual:   # type: ignore
        return NotEqual(self, make_col(other))

    def __gt__(self, other: Any) -> GreaterThan:
        return GreaterThan(self, make_col(other))

    def __ge__(self, other: Any) -> GreaterThanEqual:
        return GreaterThanEqual(self, make_col(other))

    def __lt__(self, other: Any) -> LessThan:
        return LessThan(self, make_col(other))

    def __le__(self, other: Any) -> LessThanEqual:
        return LessThanEqual(self, make_col(other))

    def is_null(self, flag: bool = True) -> IsNull:
        return IsNull(self, flag)

    def is_not_null(self, flag: bool = True) -> IsNotNull:
        return IsNotNull(self, flag)

    def is_in(self, values: Any) -> IsIn:
        return IsIn(self, make_col(values))

    def is_not_in(self, values: Any) -> IsNotIn:
        return IsNotIn(self, make_col(values))

    def asc(self, flag: bool | type[Undefined] = True) -> Ascending:
        return Ascending(self, flag)

    def desc(self, flag: bool | type[Undefined] = True) -> Descending:
        return Descending(self, flag)

    def as_(self, alias: str) -> 'AliasCol':
        return AliasCol(self, alias)

    @abstractmethod
    def __add__(self, other: Any) -> 'AddCol | UndefinedCol':
        pass

    def __radd__(self, other: Any) -> 'AddCol | UndefinedCol':
        return make_col(other) + self

    @abstractmethod
    def __sub__(self, other) -> 'SubCol | UndefinedCol':
        pass

    def __rsub__(self, other) -> 'SubCol | UndefinedCol':
        return make_col(other) - self

    @abstractmethod
    def __mul__(self, other) -> 'MulCol | UndefinedCol':
        pass

    def __rmul__(self, other) -> 'MulCol | UndefinedCol':
        return make_col(other) * self

    @abstractmethod
    def __truediv__(self, other) -> 'TrueDivCol | UndefinedCol':
        pass

    def __rtruediv__(self, other) -> 'TrueDivCol | UndefinedCol':
        return make_col(other) / self

    @abstractmethod
    def __pow__(self, power) -> 'PowCol | UndefinedCol':
        pass

    def __rpow__(self, power) -> 'PowCol | UndefinedCol':
        return make_col(power) ** self


@dataclass(repr=False, eq=False)
class UndefinedCol(Col):

    def get_composed(self) -> Composed:
        return Composed([])

    def get_inner_composed(self) -> Composed:
        return self.get_composed()

    def __add__(self, other: Any) -> 'UndefinedCol':
        return UndefinedCol()

    def __sub__(self, other) -> 'UndefinedCol':
        return UndefinedCol()

    def __mul__(self, other) -> 'UndefinedCol':
        return UndefinedCol()

    def __truediv__(self, other) -> 'UndefinedCol':
        return UndefinedCol()

    def __pow__(self, power) -> 'UndefinedCol':
        return UndefinedCol()


@dataclass(repr=False, eq=False)
class SimpleCol(Col):

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    def get_inner_composed(self) -> Composed:
        return self.get_composed()
        
    def __add__(self, other: Any) -> 'AddCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, AddCol):
            return AddCol([self] + other.cols)
        elif isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return AddCol([self, other])

    def __sub__(self, other: Any) -> 'SubCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, SubCol):
            return SubCol([self] + other.cols)
        elif isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return SubCol([self, other])

    def __mul__(self, other: Any) -> 'MulCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, MulCol):
            return MulCol([self] + other.cols)
        elif isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return MulCol([self, other])

    def __truediv__(self, other: Any) -> 'TrueDivCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, TrueDivCol):
            return TrueDivCol([self] + other.cols)
        elif isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return TrueDivCol([self, other])

    def __pow__(self, power) -> 'PowCol | UndefinedCol':
        power = make_col(power)
        if isinstance(power, PowCol):
            return PowCol([self] + power.cols)
        elif isinstance(power, UndefinedCol):
            return UndefinedCol()
        else:
            return PowCol([self, power])


@dataclass(repr=False, eq=False)
class NullCol(SimpleCol):

    def get_composed(self) -> Composed:
        return Composed([SQL('NULL')])


@dataclass(repr=False, eq=False)
class LiteralCol(SimpleCol):
    value: Any

    def get_composed(self) -> Composed:
        return SQL('{}').format(Literal(self.value))


@dataclass(repr=False, eq=False)
class SingleCol(SimpleCol):
    name: str
    tab: 'Tab | None' = None

    def get_composed(self) -> Composed:
        if self.tab:
            return SQL('{}.{}').format(self.tab.get_composed(), Identifier(self.name))
        else:
            return SQL('{}').format(Identifier(self.name))


@dataclass(repr=False, eq=False)
class ArithmeticCol(Col):
    cols: list[Col]

    @property
    @abstractmethod
    def operator(self) -> SQL:
        pass

    def get_composed(self) -> Composed:
        return self.operator.join([col.get_inner_composed() for col in self.cols])

    def get_inner_composed(self) -> Composed:
        if len(self.get_composed()._obj) > 1:
            return Composed([SQL('('), self.get_composed(), SQL(')')])
        else:
            return self.get_composed()


@dataclass(repr=False, eq=False)
class AddCol(ArithmeticCol):

    @property
    def operator(self) -> SQL:
        return SQL(' + ')

    def __add__(self, other: Any) -> 'AddCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, AddCol):
            return AddCol(self.cols + other.cols)
        elif isinstance(other, ArithmeticCol):
            return AddCol([self, other])
        elif isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return AddCol(self.cols + [other])

    def __sub__(self, other: Any) -> 'SubCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return SubCol([self, other])

    def __mul__(self, other: Any) -> 'MulCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return MulCol([self, make_col(other)])

    def __truediv__(self, other: Any) -> 'TrueDivCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return TrueDivCol([self, other])

    def __pow__(self, power: Any) -> 'PowCol | UndefinedCol':
        power = make_col(power)
        if isinstance(power, UndefinedCol):
            return UndefinedCol()
        else:
            return PowCol([self, power])


@dataclass(repr=False, eq=False)
class SubCol(ArithmeticCol):

    @property
    def operator(self) -> SQL:
        return SQL(' - ')

    def __add__(self, other: Any) -> 'AddCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return AddCol([self, other])

    def __sub__(self, other: Any) -> 'SubCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, SubCol):
            return SubCol(self.cols + other.cols)
        elif isinstance(other, ArithmeticCol):
            return SubCol([self, other])
        elif isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return SubCol(self.cols + [other])

    def __mul__(self, other: Any) -> 'MulCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return MulCol([self, other])

    def __truediv__(self, other: Any) -> 'TrueDivCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return TrueDivCol([self, other])

    def __pow__(self, power: Any) -> 'PowCol | UndefinedCol':
        power = make_col(power)
        if isinstance(power, UndefinedCol):
            return UndefinedCol()
        else:
            return PowCol([self, power])


@dataclass(repr=False, eq=False)
class MulCol(ArithmeticCol):

    @property
    def operator(self) -> SQL:
        return SQL(' * ')

    def __add__(self, other: Any) -> 'AddCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return AddCol([self, other])

    def __sub__(self, other: Any) -> 'SubCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return SubCol([self, other])

    def __mul__(self, other: Any) -> 'MulCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, MulCol):
            return MulCol(self.cols + other.cols)
        elif isinstance(other, ArithmeticCol):
            return MulCol([self, other])
        elif isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return MulCol(self.cols + [other])

    def __truediv__(self, other: Any) -> 'TrueDivCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return TrueDivCol([self, other])

    def __pow__(self, power: Any) -> 'PowCol | UndefinedCol':
        power = make_col(power)
        if isinstance(power, UndefinedCol):
            return UndefinedCol()
        else:
            return PowCol([self, power])


@dataclass(repr=False, eq=False)
class TrueDivCol(ArithmeticCol):

    @property
    def operator(self) -> SQL:
        return SQL(' / ')

    def __add__(self, other: Any) -> 'AddCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return AddCol([self, other])

    def __sub__(self, other: Any) -> 'SubCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return SubCol([self, other])

    def __mul__(self, other: Any) -> 'MulCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return MulCol([self, other])

    def __truediv__(self, other: Any) -> 'TrueDivCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, TrueDivCol):
            return TrueDivCol(self.cols + other.cols)
        elif isinstance(other, ArithmeticCol):
            return TrueDivCol([self, other])
        elif isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return TrueDivCol(self.cols + [other])

    def __pow__(self, power: Any) -> 'PowCol | UndefinedCol':
        power = make_col(power)
        if isinstance(power, UndefinedCol):
            return UndefinedCol()
        else:
            return PowCol([self, power])


@dataclass(repr=False, eq=False)
class PowCol(ArithmeticCol):

    @property
    def operator(self) -> SQL:
        return SQL(' ^ ')

    def __add__(self, other: Any) -> 'AddCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return AddCol([self, other])

    def __sub__(self, other: Any) -> 'SubCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return SubCol([self, other])

    def __mul__(self, other: Any) -> 'MulCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return MulCol([self, other])

    def __truediv__(self, other: Any) -> 'TrueDivCol | UndefinedCol':
        other = make_col(other)
        if isinstance(other, UndefinedCol):
            return UndefinedCol()
        else:
            return TrueDivCol([self, other])

    def __pow__(self, power: Any) -> 'PowCol | UndefinedCol':
        power = make_col(power)
        if isinstance(power, PowCol):
            return PowCol(self.cols + power.cols)
        elif isinstance(power, ArithmeticCol):
            return PowCol([self, power])
        elif isinstance(power, UndefinedCol):
            return UndefinedCol()
        else:
            return PowCol(self.cols + [power])


@dataclass(repr=False, eq=False)
class AliasCol(Col):
    col: Col
    alias: str

    @abstractmethod
    def get_composed(self) -> Composed:
        return SQL('{} AS {}').format(self.col.get_composed(), Identifier(self.alias))

    def __add__(self, other: Any) -> 'AddCol | UndefinedCol':
        return self.col.__add__(other)

    def __sub__(self, other) -> 'SubCol | UndefinedCol':
        return self.col.__sub__(other)

    def __mul__(self, other) -> 'MulCol | UndefinedCol':
        return self.col.__mul__(other)

    def __truediv__(self, other) -> 'TrueDivCol | UndefinedCol':
        return self.col.__truediv__(other)

    def __pow__(self, power) -> 'PowCol | UndefinedCol':
        return self.col.__pow__(power)


@dataclass(repr=False, eq=False)
class FunCol(SimpleCol):

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


@dataclass(repr=False, eq=False)
class SumCol(FunCol):
    col: Col

    def get_composed(self) -> Composed:
        return SQL('sum({})').format(self.col.get_composed())


@dataclass(repr=False, eq=False)
class AvgCol(FunCol):
    col: Col

    def get_composed(self) -> Composed:
        return SQL('avg({})').format(self.col.get_composed())


@dataclass(repr=False, eq=False)
class ToJsonCol(FunCol):
    tab: 'Tab'

    def get_composed(self) -> Composed:
        return SQL('to_json({})').format(self.tab.get_composed())


@dataclass(repr=False, eq=False)
class JsonAggCol(FunCol):
    value: 'Tab | Col'

    def get_composed(self) -> Composed:
        return SQL('json_agg({})').format(self.value.get_composed())
