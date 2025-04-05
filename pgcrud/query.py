from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Self

from pgcrud.clauses import (
    Clause,
    FromClause,
    SelectClause,
    WhereClause,
    GroupByClause,
    HavingClause,
    WindowClause,
    OrderByClause,
    LimitClause,
    OffsetClause,
    InsertIntoClause,
    ReturningClause,
    UpdateClause,
    DeleteFromClause,
    PartitionByClause,
    ValuesClause,
    SetClause,
    UsingClause,
    RowsBetweenClause,
    RangeBetweenClause,
    WithClause,
    OnConflictExpression,
    DoNothingClause,
    OnConstraintClause,
    DoUpdateClause,
)
from pgcrud.expressions.base import (
    make_expr,
    IdentifierExpression,
    AsClauseExpression,
)
from pgcrud.expressions.base import QueryExpression
from pgcrud.utils import ensure_seq


__all__ = ['Query']


class Query:

    def __init__(self, clauses: list[Clause]):
        self.clauses = clauses

    def __str__(self):
        return ' '.join([str(clause) for clause in self.clauses if clause])

    def __repr__(self):
        return str(self)

    @property
    def _expr(self) -> QueryExpression:
        return QueryExpression(self)

    def merge(self, query: Query) -> Self:
        self.clauses += query.clauses
        return self

    def AS(self, value: Any) -> AsClauseExpression:
        return AsClauseExpression(QueryExpression(self), value)

    def DELETE_FROM(self, value: Any) -> Self:
        self.clauses.append(DeleteFromClause(make_expr(value)))
        return self

    @property
    def DO_NOTHING(self) -> Self:
        self.clauses.append(DoNothingClause())
        return self

    @property
    def DO_UPDATE(self) -> Self:
        self.clauses.append(DoUpdateClause())
        return self

    def FROM(self, value: Any) -> Self:
        self.clauses.append(FromClause(make_expr(value)))
        return self

    def GROUP_BY(self, *args: Any) -> Self:
        self.clauses.append(GroupByClause([make_expr(arg) for arg in args]))
        return self

    def HAVING(self, value: Any) -> Self:
        self.clauses.append(HavingClause(make_expr(value)))
        return self

    def INSERT_INTO(self, value: IdentifierExpression) -> Self:
        self.clauses.append(InsertIntoClause(value))
        return self

    def LIMIT(self, value: int) -> Self:
        self.clauses.append(LimitClause(value))
        return self

    def OFFSET(self, value: int) -> Self:
        self.clauses.append(OffsetClause(value))
        return self

    @property
    def ON_CONFLICT(self) -> Self:
        self.clauses.append(OnConflictExpression())
        return self

    def ON_CONSTRAINT(self, value: Any) -> Self:
        self.clauses.append(OnConstraintClause(make_expr(value)))
        return self

    def ORDER_BY(self, *args: Any) -> Self:
        self.clauses.append(OrderByClause([make_expr(arg) for arg in args]))
        return self

    def PARTITION_BY(self, *args: Any) -> Self:
        self.clauses.append(PartitionByClause([make_expr(arg) for arg in args]))
        return self

    def RANGE_BETWEEN(self, start: Any, end: Any) -> Self:
        self.clauses.append(RangeBetweenClause(make_expr(start), make_expr(end)))
        return self

    def RETURNING(self, *args: Any) -> Self:
        self.clauses.append(ReturningClause([make_expr(arg) for arg in args]))
        return self

    def ROWS_BETWEEN(self, start: Any, end: Any) -> Self:
        self.clauses.append(RowsBetweenClause(make_expr(start), make_expr(end)))
        return self

    def SELECT(self, *args: Any) -> Self:
        self.clauses.append(SelectClause([make_expr(arg) for arg in args]))
        return self

    def SET(self, columns: IdentifierExpression | Sequence[IdentifierExpression], values: Any, **kwargs: Any) -> Self:
        self.clauses.append(SetClause(ensure_seq(columns), values, kwargs))
        return self

    def UPDATE(self, value: Any) -> Self:
        self.clauses.append(UpdateClause(make_expr(value)))
        return self

    def USING(self, value: Any) -> Self:
        self.clauses.append(UsingClause(make_expr(value)))
        return self

    def VALUES(self, *args: Any, **kwargs: Any) -> Self:
        order = None
        if len(self.clauses) > 0:
            clause = self.clauses[-1]
            if isinstance(clause, InsertIntoClause):
                order = clause.identifier_expression._columns
        self.clauses.append(ValuesClause(args, kwargs, order))
        return self

    def WINDOW(self, *args: Any) -> Self:
        self.clauses.append(WindowClause([make_expr(arg) for arg in args]))
        return self

    def WITH(self, *args: Any) -> Self:
        self.clauses.append(WithClause([make_expr(arg) for arg in args]))
        return self

    def WHERE(self, value: Any) -> Self:
        self.clauses.append(WhereClause(make_expr(value)))
        return self
