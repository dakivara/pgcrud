from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pgcrud.clauses import (
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
    Set,
    Using,
    With,
    RowsBetween, RangeBetween,
)
from pgcrud.expressions import (
    CurrentRow,
    Unbounded,
    Expression,
    Literal,
    Identifier,
    make_expr,
    TableIdentifier,
)
from pgcrud.filter_conditions import FilterCondition
from pgcrud.query import Query
from pgcrud.utils import ensure_seq


__all__ = ['QueryBuilder']


class QueryBuilder:

    def __new__(cls):
        raise TypeError("'QueryBuilder' object is not callable")

    @staticmethod
    def DELETE_FROM(identifier: Identifier) -> Query:
        return Query([DeleteFrom(identifier)])

    @staticmethod
    def FROM(expression: Expression) -> Query:
        return Query([From(expression)])

    @staticmethod
    def GROUP_BY(*args: Any | Expression) -> Query:
        return Query([GroupBy([make_expr(arg) for arg in args])])

    @staticmethod
    def HAVING(condition: FilterCondition) -> Query:
        return Query([Having(condition)])

    @staticmethod
    def INSERT_INTO(identifier: Identifier | TableIdentifier) -> Query:
        return Query([InsertInto(identifier)])

    @staticmethod
    def LIMIT(value: int) -> Query:
        return Query([Limit(value)])

    @staticmethod
    def OFFSET(value: int) -> Query:
        return Query([Offset(value)])

    @staticmethod
    def ORDER_BY(*args: Expression) -> Query:
        return Query([OrderBy([make_expr(arg) for arg in args])])

    @staticmethod
    def PARTITION_BY(*args: Expression) -> Query:
        return Query([PartitionBy(args)])

    @staticmethod
    def RANGE_BETWEEN(start: Literal | Unbounded | CurrentRow, end: Literal | Unbounded | CurrentRow) -> Query:
        return Query([RangeBetween(start, end)])

    @staticmethod
    def RETURNING(*args: Any | Expression) -> Query:
        return Query([Returning([make_expr(arg) for arg in args])])

    @staticmethod
    def ROWS_BETWEEN(start: Literal | Unbounded | CurrentRow, end: Literal | Unbounded | CurrentRow) -> Query:
        return Query([RowsBetween(start, end)])

    @staticmethod
    def SELECT(*args: Any | Expression) -> Query:
        return Query([Select([make_expr(arg) for arg in args])])

    @staticmethod
    def SET(columns: Identifier | Sequence[Identifier], values: Any, **kwargs: Any) -> Query:
        return Query([Set(ensure_seq(columns), values, kwargs)])

    @staticmethod
    def UPDATE(identifier: Identifier) -> Query:
        return Query([Update(identifier)])

    @staticmethod
    def USING(expression: Expression) -> Query:
        return Query([Using(expression)])

    @staticmethod
    def VALUES(*args: Any, **kwargs: Any) -> Query:
        return Query([Values(args, kwargs)])

    @staticmethod
    def WINDOW(*args: Identifier) -> Query:
        return Query([Window(args)])

    @staticmethod
    def WITH(*args: Identifier) -> Query:
        return Query([With(args)])

    @staticmethod
    def WHERE(condition: FilterCondition) -> Query:
        return Query([Where(condition)])
