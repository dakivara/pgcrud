from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pgcrud.clauses import (
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
    WithClause,
    RowsBetweenClause,
    RangeBetweenClause,
    DoNothingClause,
    OnConflictExpression, OnConstraintClause, DoUpdateClause,
)

from pgcrud.expressions.base import (
    make_expr,
    IdentifierExpression
)

from pgcrud.query import Query
from pgcrud.utils import ensure_seq


__all__ = ['QueryBuilder']


class QueryBuilderType(type):

    @property
    def DO_NOTHING(cls) -> Query:
        return Query([DoNothingClause()])

    @property
    def DO_UPDATE(cls) -> Query:
        return Query([DoUpdateClause()])

    @property
    def ON_CONFLICT(cls) -> Query:
        return Query([OnConflictExpression()])


class QueryBuilder(metaclass=QueryBuilderType):

    def __new__(cls):
        raise TypeError("'QueryBuilder' object is not callable")

    @staticmethod
    def DELETE_FROM(value: Any) -> Query:
        return Query([DeleteFromClause(value)])

    @staticmethod
    def FROM(value: Any) -> Query:
        return Query([FromClause(make_expr(value))])

    @staticmethod
    def GROUP_BY(*args: Any) -> Query:
        return Query([GroupByClause([make_expr(arg) for arg in args])])

    @staticmethod
    def HAVING(value: Any) -> Query:
        return Query([HavingClause(make_expr(value))])

    @staticmethod
    def INSERT_INTO(value: IdentifierExpression) -> Query:
        return Query([InsertIntoClause(value)])

    @staticmethod
    def LIMIT(value: int) -> Query:
        return Query([LimitClause(value)])

    @staticmethod
    def OFFSET(value: int) -> Query:
        return Query([OffsetClause(value)])

    @staticmethod
    def ON_CONSTRAINT(value: Any) -> Query:
        return Query([OnConstraintClause(make_expr(value))])

    @staticmethod
    def ORDER_BY(*args: Any) -> Query:
        return Query([OrderByClause([make_expr(arg) for arg in args])])

    @staticmethod
    def PARTITION_BY(*args: Any) -> Query:
        return Query([PartitionByClause([make_expr(arg) for arg in args])])

    @staticmethod
    def RANGE_BETWEEN(start: Any, end: Any) -> Query:
        return Query([RangeBetweenClause(make_expr(start), make_expr(end))])

    @staticmethod
    def RETURNING(*args: Any) -> Query:
        return Query([ReturningClause([make_expr(arg) for arg in args])])

    @staticmethod
    def ROWS_BETWEEN(start: Any, end: Any) -> Query:
        return Query([RowsBetweenClause(make_expr(start), make_expr(end))])

    @staticmethod
    def SELECT(*args: Any) -> Query:
        return Query([SelectClause([make_expr(arg) for arg in args])])

    @staticmethod
    def SET(columns: IdentifierExpression | Sequence[IdentifierExpression], values: Any, **kwargs: Any) -> Query:
        return Query([SetClause(ensure_seq(columns), values, kwargs)])

    @staticmethod
    def UPDATE(value: Any) -> Query:
        return Query([UpdateClause(make_expr(value))])

    @staticmethod
    def USING(value: Any) -> Query:
        return Query([UsingClause(make_expr(value))])

    @staticmethod
    def VALUES(*args: Any, **kwargs: Any) -> Query:
        return Query([ValuesClause(args, kwargs)])

    @staticmethod
    def WINDOW(*args: Any) -> Query:
        return Query([WindowClause([make_expr(arg) for arg in args])])

    @staticmethod
    def WITH(*args: Any) -> Query:
        return Query([WithClause([make_expr(arg) for arg in args])])

    @staticmethod
    def WHERE(value: Any) -> Query:
        return Query([WhereClause(make_expr(value))])
