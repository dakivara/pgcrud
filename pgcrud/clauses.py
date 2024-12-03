from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass

from psycopg.sql import SQL, Composed, Literal
from pydantic import BaseModel

from pgcrud.expr import Expr, ReferenceExpr
from pgcrud.operators import SortOperator
from pgcrud.types import AdditionalValuesType, DeleteFromValueType, FromValueType, GroupByValueType, HavingValueType, InsertIntoValueType, OrderByValueType, ReturningValueType, SelectValueType, SetColsType, SetValuesType, UpdateValueType, UsingValueType, ValuesValueType, WhereValueType
from pgcrud.utils import ensure_seq


__all__ = [
    'Clause',
    'Select',
    'From',
    'Where',
    'GroupBy',
    'Having',
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
    value: SelectValueType

    def __bool__(self) -> bool:
        return bool(self.exprs)

    def __post_init__(self):
        
        exprs: list[Expr] = []

        if isinstance(self.value, type) and issubclass(self.value, BaseModel):
            for name, field in self.value.model_fields.items():
                expr = ReferenceExpr(name)

                for m in field.metadata:
                    if isinstance(m, Expr):
                        expr = m
                        break

                if expr:
                    exprs.append(expr)

        else:
            for expr in ensure_seq(self.value):
                if expr:
                    exprs.append(expr)

        self.exprs = exprs

    def get_composed(self) -> Composed:
        return SQL('SELECT {}').format(SQL(', ').join([expr.get_composed() for expr in self.exprs]))


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
        return bool(self.exprs)

    def __post_init__(self):

        exprs: list[Expr] = []

        for expr in ensure_seq(self.value):
            if expr:
                exprs.append(expr)

        self.exprs = exprs

    def get_composed(self) -> Composed:
        return SQL('GROUP BY {}').format(SQL(', ').join([expr.get_composed() for expr in self.exprs]))


@dataclass(repr=False)
class Having(Clause):
    value: HavingValueType

    def __bool__(self) -> bool:
        return bool(self.value)

    def get_composed(self) -> Composed:
        return SQL('HAVING {}').format(self.value.get_composed())


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

        composed_vals = []

        for vals in self.value:
            if isinstance(vals, Sequence):
                vals = [Literal(val) for val in vals]
            elif isinstance(vals, dict):
                params = self.additional_values.copy()
                params.update(vals)
                vals = [Literal(params.get(expr._name)) for expr in self.get_exprs()]
            else:
                params = self.additional_values.copy()
                params.update(vals.model_dump(by_alias=True))
                vals = [Literal(params.get(expr._name)) for expr in self.get_exprs()]

            composed_vals.append(SQL('({})').format(SQL(', ').join(vals)))

        return SQL('VALUES {}').format(SQL(', ').join(composed_vals))

    def get_exprs(self) -> tuple['ReferenceExpr', ...]:
        if self._prev_clause:
            return self._prev_clause.value.children
        else:
            return ()


@dataclass(repr=False)
class Returning(Clause):
    value: ReturningValueType

    def __bool__(self) -> bool:
        return bool(self.exprs)

    def __post_init__(self):

        exprs: list[Expr] = []

        if isinstance(self.value, type) and issubclass(self.value, BaseModel):
            for name, field in self.value.model_fields.items():
                expr = ReferenceExpr(name)

                for m in field.metadata:
                    if isinstance(m, Expr):
                        expr = m
                        break

                if expr:
                    exprs.append(expr)

        else:
            for expr in ensure_seq(self.value):
                if expr:
                    exprs.append(expr)

        self.exprs = exprs

    def get_composed(self) -> Composed:
        return SQL('RETURNING {}').format(SQL(', ').join([expr.get_composed() for expr in self.exprs]))


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
        composed_values = []

        if isinstance(self.values, Sequence):
            for v in self.values:
                composed_values.append(Literal(v))

        elif isinstance(self.values, dict):
            params = self.additional_values.copy()
            params.update(self.values)

            for expr in self.cols:
                composed_values.append(Literal(params.get(expr._name)))

        else:
            params = self.additional_values.copy()
            params.update(self.values.model_dump(by_alias=True))

            for expr in self.cols:
                composed_values.append(Literal(params.get(expr._name)))

        composed_values = SQL(', ').join(composed_values)

        if len(self.cols) > 1:
            return SQL('SET ({}) = ({})').format(composed_cols, composed_values)
        else:
            return SQL('SET {} = {}').format(composed_cols, composed_values)


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
