from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Self

from pgcrud.clauses import (
    Clause,
    From,
    Select,
    Where,
    GroupBy,
    Having,
    Window,
    OrderBy,
    Limit,
    Offset,
    InsertInto,
    Returning,
    Update,
    DeleteFrom,
    PartitionBy,
    Values,
    Set, Using, RowsBetween, RangeBetween,
    With, OnConflict, DoNothing, OnConstraint, DoUpdate,
)
from pgcrud.expressions import (
    CurrentRow,
    Expression,
    Literal,
    Identifier,
    DerivedTable,
    TableIdentifier,
    Unbounded,
    make_expr,
)
from pgcrud.filter_conditions import FilterCondition
from pgcrud.utils import ensure_seq


__all__ = ['Query']


class Query:

    _tag = 'QUERY'

    def __init__(self, clauses: list[Clause]):
        self._clauses = clauses

    def __str__(self):
        return ' '.join([str(clause) for clause in self._clauses if clause])

    def __repr__(self):
        return str(self)

    def merge(self, query: Query) -> Self:
        self._clauses += query._clauses
        return self

    def AS(self, identifier: Identifier) -> DerivedTable:
        return DerivedTable(self).AS(identifier)

    def DELETE_FROM(self, identifier: Identifier) -> Self:
        self._clauses.append(DeleteFrom(identifier))
        return self

    @property
    def DO_NOTHING(self) -> Self:
        self._clauses.append(DoNothing())
        return self

    @property
    def DO_UPDATE(self) -> Self:
        self._clauses.append(DoUpdate())
        return self

    def FROM(self, expression: Expression) -> Self:
        self._clauses.append(From(make_expr(expression)))
        return self

    def GROUP_BY(self, *args: Any | Expression) -> Self:
        self._clauses.append(GroupBy([make_expr(arg) for arg in args]))
        return self

    def HAVING(self, condition: FilterCondition) -> Self:
        self._clauses.append(Having(condition))
        return self

    def INSERT_INTO(self, identifier: Identifier | TableIdentifier) -> Self:
        self._clauses.append(InsertInto(identifier))
        return self

    def LIMIT(self, value: int) -> Self:
        self._clauses.append(Limit(value))
        return self

    def OFFSET(self, value: int) -> Self:
        self._clauses.append(Offset(value))
        return self

    @property
    def ON_CONFLICT(self) -> Self:
        self._clauses.append(OnConflict())
        return self

    def ON_CONSTRAINT(self, identifier: Identifier) -> Self:
        self._clauses.append(OnConstraint(identifier))
        return self

    def ORDER_BY(self, *args: Any | Expression) -> Self:
        self._clauses.append(OrderBy([make_expr(arg) for arg in args]))
        return self

    def PARTITION_BY(self, *args: Expression) -> Self:
        self._clauses.append(PartitionBy(args))
        return self

    def RANGE_BETWEEN(self, start: Literal | Unbounded | CurrentRow, end: Literal | Unbounded | CurrentRow) -> Self:
        self._clauses.append(RangeBetween(start, end))
        return self

    def RETURNING(self, *args: Any | Expression) -> Self:
        self._clauses.append(Returning([make_expr(arg) for arg in args]))
        return self

    def ROWS_BETWEEN(self, start: Literal | Unbounded | CurrentRow, end: Literal | Unbounded | CurrentRow) -> Self:
        self._clauses.append(RowsBetween(start, end))
        return self

    def SELECT(self, *args: Any | Expression) -> Self:
        self._clauses.append(Select([make_expr(arg) for arg in args]))
        return self

    def SET(self, columns: Identifier | Sequence[Identifier], values: Any, **kwargs: Any) -> Self:
        self._clauses.append(Set(ensure_seq(columns), values, kwargs))
        return self

    def UPDATE(self, identifier: Identifier) -> Self:
        self._clauses.append(Update(identifier))
        return self

    def USING(self, expression: Expression) -> Self:
        self._clauses.append(Using(expression))
        return self

    def VALUES(self, *args: Any, **kwargs: Any) -> Self:
        order = None
        if len(self._clauses) > 0:
            clause = self._clauses[-1]
            if isinstance(clause, InsertInto):
                if isinstance(clause.identifier, TableIdentifier):
                    order = clause.identifier._columns
        self._clauses.append(Values(args, kwargs, order))
        return self

    def WINDOW(self, *args: Identifier) -> Self:
        self._clauses.append(Window(args))
        return self

    def WITH(self, *args: Identifier) -> Self:
        self._clauses.append(With(args))
        return self

    def WHERE(self, condition: FilterCondition) -> Self:
        self._clauses.append(Where(condition))
        return self
