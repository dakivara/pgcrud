from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from psycopg.sql import SQL, Identifier, Composed, Literal

from pgcrud._operators.assign_operator import *
from pgcrud._operators.filter_operators import *
from pgcrud._operators.sort_operators import *
from pgcrud._undefined import Undefined

if TYPE_CHECKING:
    from pgcrud._tab import Tab


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

    @property
    def is_undefined_col(self) -> bool:
        return isinstance(self, UndefinedCol)

    @abstractmethod
    def get_composed(self) -> Composed:
        pass

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

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

    def __lshift__(self, other: Any) -> Assign:
        return Assign(self, make_col(other))

    def is_null(self, flag: bool = True) -> IsNull:
        return IsNull(self, flag)

    def is_not_null(self, flag: bool = True) -> IsNotNull:
        return IsNotNull(self, flag)

    def is_in(self, values: Any) -> IsIn:
        return IsIn(self, make_col(values))

    def is_not_in(self, values: Any) -> IsNotIn:
        return IsNotIn(self, make_col(values))

    def asc(self, flag: bool = True) -> Ascending:
        return Ascending(self, flag)

    def desc(self, flag: bool = True) -> Descending:
        return Descending(self, flag)

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

    @abstractmethod
    def get_composed(self) -> Composed:
        return Composed([])

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
    table: 'Tab | None' = None

    def get_composed(self) -> Composed:
        if self.table:
            return SQL('{}.{}').format(Identifier(self.table.name), Identifier(self.name))
        else:
            return SQL('{}').format(Identifier(self.name))


@dataclass(repr=False, eq=False)
class ArithmeticCol(Col):
    cols: list[Col]

    @property
    @abstractmethod
    def operator(self) -> SQL:
        pass

    def get_composed(self, _inner: bool = False) -> Composed:
        composed_list = []

        for col in self.cols:
            if isinstance(col, ArithmeticCol):
                composed_list.append(col.get_composed(True))
            elif isinstance(col, SimpleCol):
                composed_list.append(col.get_composed())
            else:
                composed_list.append(SQL('{}').format(Literal(col)))

        composed = self.operator.join(composed_list)

        if len(composed_list) > 1 and _inner:
            composed = Composed([SQL('('), composed, SQL(')')])

        return composed


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
