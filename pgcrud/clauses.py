from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from psycopg.sql import SQL, Composed, Literal

from pgcrud.expr import Expr, ReferenceExpr, AliasExpr, make_expr
from pgcrud.frame_boundaries import FrameBoundary
from pgcrud.operators import SortOperator
from pgcrud.optional_dependencies import is_pydantic_installed, is_pydantic_instance, is_msgspec_installed, is_msgspec_instance, msgspec_to_dict, pydantic_to_dict
from pgcrud.types import AdditionalValuesType, DeleteFromValueType, FromValueType, GroupByValueType, HavingValueType, InsertIntoValueType, OrderByValueType, PartitionByValueType, ReturningValueType, SelectValueType, SetColsType, SetValuesType, UpdateValueType, UsingValueType, ValuesValueType, WhereValueType, WindowValueType
from pgcrud.utils import ensure_seq


__all__ = [
    'Clause',
    'Select',
    'From',
    'Where',
    'GroupBy',
    'Having',
    'Window',
    'OrderBy',
    'Limit',
    'Offset',
    'InsertInto',
    'Values',
    'Returning',
    'Update',
    'Set',
    'DeleteFrom',
    'Using',
    'PartitionBy',
    'RowsBetween',
    'With',
]


@dataclass
class Clause:

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return str(self)

    @abstractmethod
    def __bool__(self) -> bool:
        pass

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


@dataclass(repr=False)
class Select(Clause):
    value: Sequence[Any | Expr]

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('SELECT {}').format(SQL(', ').join([make_expr(v).get_composed() for v in self.value]))


@dataclass(repr=False)
class From(Clause):
    value: FromValueType

    def __bool__(self) -> bool:
        return bool(self.value)

    def get_composed(self) -> Composed:
        return SQL('FROM {}').format(self.value.get_composed())


@dataclass(repr=False)
class Where(Clause):
    value: WhereValueType

    def __bool__(self) -> bool:
        return bool(self.value)

    def get_composed(self) -> Composed:
        return SQL('WHERE {}').format(self.value.get_composed())


@dataclass(repr=False)
class GroupBy(Clause):
    value: GroupByValueType

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('GROUP BY {}').format(SQL(', ').join([expr.get_composed() for expr in ensure_seq(self.value)]))


@dataclass(repr=False)
class Having(Clause):
    value: HavingValueType

    def __bool__(self) -> bool:
        return bool(self.value)

    def get_composed(self) -> Composed:
        return SQL('HAVING {}').format(self.value.get_composed())


@dataclass(repr=False)
class Window(Clause):
    value: WindowValueType

    def __bool__(self) -> bool:
        return bool(self.value)

    def get_composed(self) -> Composed:
        return SQL('WINDOW {}').format(SQL(', ').join([v.get_composed() for v in ensure_seq(self.value)]))


@dataclass(repr=False)
class OrderBy(Clause):
    value: OrderByValueType

    def __bool__(self) -> bool:
        return bool(self.exprs)

    def __post_init__(self):

        exprs: list[Expr | SortOperator] = []

        for expr in ensure_seq(self.value):
            if expr:
                exprs.append(expr)

        self.exprs = exprs

    def get_composed(self) -> Composed:
        return SQL('ORDER BY {}').format(SQL(', ').join([expr.get_composed() for expr in self.exprs]))


@dataclass(repr=False)
class Limit(Clause):
    value: int

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('LIMIT {}').format(self.value)


@dataclass(repr=False)
class Offset(Clause):
    value: int

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('OFFSET {}').format(self.value)


@dataclass(repr=False)
class InsertInto(Clause):
    value: InsertIntoValueType

    def __bool__(self) -> bool:
        return bool(self.value.children)

    def get_composed(self) -> Composed:
        return SQL('INSERT INTO {}').format(self.value.get_composed())


@dataclass(repr=False)
class Values(Clause):
    value: tuple[ValuesValueType, ...]
    additional_values: AdditionalValuesType
    _prev_clause: InsertInto | None = None

    def __bool__(self) -> bool:
        return bool(self.value)

    def get_composed(self) -> Composed:

        vals_composed_list = []

        for vals in self.value:

            if is_msgspec_installed and is_msgspec_instance(vals):
                params = self.additional_values.copy()
                params.update(msgspec_to_dict(vals))  # type: ignore
                vals_composed = SQL(', ').join([Literal(params.get(expr._name)) for expr in self.get_exprs()])

            elif is_pydantic_installed and is_pydantic_instance(vals):
                params = self.additional_values.copy()
                params.update(pydantic_to_dict(vals))  # type: ignore
                vals_composed = SQL(', ').join([Literal(params.get(expr._name)) for expr in self.get_exprs()])

            elif isinstance(vals, dict):
                params = self.additional_values.copy()
                params.update(vals)
                vals_composed = SQL(', ').join([Literal(params.get(expr._name)) for expr in self.get_exprs()])

            elif isinstance(vals, Sequence):
                vals_composed =  SQL(', ').join([Literal(val) for val in vals])

            else:
                vals_composed = SQL(', ').join([vals])

            vals_composed_list.append(SQL('({})').format(SQL(', ').join(vals_composed)))

        return SQL('VALUES {}').format(SQL(', ').join(vals_composed_list))

    def get_exprs(self) -> tuple['ReferenceExpr', ...]:
        if self._prev_clause:
            return self._prev_clause.value.children
        else:
            return ()


@dataclass(repr=False)
class Returning(Clause):
    value: ReturningValueType

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('RETURNING {}').format(SQL(', ').join([make_expr(v).get_composed() for v in ensure_seq(self.value)]))


@dataclass(repr=False)
class Update(Clause):
    value: UpdateValueType

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('UPDATE {}').format(self.value.get_composed())


@dataclass(repr=False)
class Set(Clause):
    cols: SetColsType
    values: SetValuesType
    additional_values: AdditionalValuesType

    def __bool__(self) -> bool:
        return bool(self.cols)

    def get_composed(self) -> Composed:

        composed_cols = SQL(', ').join([expr.get_composed() for expr in self.cols])

        if is_msgspec_installed and is_msgspec_instance(self.values):
            params = self.additional_values.copy()
            params.update(msgspec_to_dict(self.values))  # type: ignore
            vals_composed = SQL(', ').join([Literal(params.get(expr._name)) for expr in self.cols])

        elif is_pydantic_installed and is_pydantic_instance(self.values):
            params = self.additional_values.copy()
            params.update(pydantic_to_dict(self.values))  # type: ignore
            vals_composed = SQL(', ').join([Literal(params.get(expr._name)) for expr in self.cols])

        elif isinstance(self.values, dict):
            params = self.additional_values.copy()
            params.update(self.values)
            vals_composed = SQL(', ').join([Literal(params.get(expr._name)) for expr in self.cols])

        elif isinstance(self.values, Sequence):
            vals_composed = SQL(', ').join([Literal(v) for v in self.values])

        else:
            vals_composed = SQL(', ').join([self.values])

        if len(self.cols) > 1:
            return SQL('SET ({}) = ({})').format(composed_cols, vals_composed)
        else:
            return SQL('SET {} = {}').format(composed_cols, vals_composed)


@dataclass(repr=False)
class DeleteFrom(Clause):
    value: DeleteFromValueType

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('DELETE FROM {}').format(self.value.get_composed())


@dataclass(repr=False)
class Using(Clause):
    value: UsingValueType

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('USING {}').format(self.value.get_composed())


@dataclass(repr=False)
class PartitionBy(Clause):
    value: PartitionByValueType

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('PARTITION BY {}').format(SQL(', ').join([expr.get_composed() for expr in ensure_seq(self.value)]))


@dataclass(repr=False)
class RowsBetween(Clause):
    start: FrameBoundary
    end: FrameBoundary

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('ROWS BETWEEN {} AND {}').format(self.start.get_composed(), self.end.get_composed())


@dataclass(repr=False)
class RangeBetween(Clause):
    start: FrameBoundary
    end: FrameBoundary

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('RANGE BETWEEN {} AND {}').format(self.start.get_composed(), self.end.get_composed())


@dataclass(repr=False)
class With(Clause):
    exprs: tuple[AliasExpr, ...]

    def __bool__(self) -> bool:
        return True

    def get_composed(self) -> Composed:
        return SQL('WITH {}').format(SQL(', ').join([expr.get_composed() for expr in self.exprs]))
