from collections.abc import Sequence
from typing import Any

from psycopg.sql import Placeholder

from pgcrud.clauses import From, RowsBetween, Select, Where, GroupBy, Having, OrderBy, Limit, Offset, InsertInto, Values, Update, Set, DeleteFrom, Using, PartitionBy, With, RangeBetween, Window, Returning
from pgcrud.expr import Expr, AliasExpr, PlaceholderExpr, ReferenceExpr, TableReferenceExpr, make_expr
from pgcrud.frame_boundaries import FrameBoundary
from pgcrud.operators import FilterOperator, SortOperator
from pgcrud.query import Query
from pgcrud.utils import ensure_seq


__all__ = ['QueryBuilder']


class QueryBuilder:

    def __new__(cls):
        raise TypeError("'QueryBuilder' object is not callable")

    @staticmethod
    def SELECT(*args: Any | Expr) -> Query:
        return Query([Select([make_expr(v) for v in args])])

    @staticmethod
    def FROM(value: Expr) -> Query:
        return Query([From(value)])

    @staticmethod
    def WHERE(value: FilterOperator) -> Query:
        return Query([Where(value)])

    @staticmethod
    def GROUP_BY(*args: Any | Expr) -> Query:
        return Query([GroupBy([make_expr(v) for v in args])])

    @staticmethod
    def HAVING(value: FilterOperator) -> Query:
        return Query([Having(value)])

    @staticmethod
    def WINDOW(*args: AliasExpr) -> Query:
        return Query([Window(args)])

    @staticmethod
    def ORDER_BY(*args: Any | Expr | SortOperator) -> Query:
        return Query([OrderBy([v if isinstance(v, (Expr, SortOperator)) else make_expr(v) for v in args])])

    @staticmethod
    def LIMIT(value: int) -> Query:
        return Query([Limit(value)])

    @staticmethod
    def OFFSET(value: int) -> Query:
        return Query([Offset(value)])

    @staticmethod
    def INSERT_INTO(value: TableReferenceExpr) -> Query:
        return Query([InsertInto(value)])

    @staticmethod
    def VALUES(*args: Any | Sequence[Any] | dict[str, Any], **kwargs: Any) -> Query:
        return Query([Values(args, kwargs)])

    @staticmethod
    def RETURNING(*args: Any | Expr) -> Query:
        return Query([Returning([make_expr(v) for v in args])])

    @staticmethod
    def UPDATE(value: ReferenceExpr) -> Query:
        return Query([Update(value)])

    @staticmethod
    def SET(cols: ReferenceExpr | Sequence[ReferenceExpr], values: Any | Sequence | dict[str, Any], **kwargs: Any) -> Query:
        return Query([Set(ensure_seq(cols), values, kwargs)])

    @staticmethod
    def DELETE_FROM(value: ReferenceExpr) -> Query:
        return Query([DeleteFrom(value)])

    @staticmethod
    def USING(value: Expr) -> Query:
        return Query([Using(value)])

    @staticmethod
    def PARTITION_BY(*args: Expr) -> Query:
        return Query([PartitionBy(args)])

    @staticmethod
    def ROWS_BETWEEN(start: FrameBoundary, end: FrameBoundary) -> Query:
        return Query([RowsBetween(start, end)])

    @staticmethod
    def RANGE_BETWEEN(start: FrameBoundary, end: FrameBoundary) -> Query:
        return Query([RangeBetween(start, end)])

    @staticmethod
    def WITH(*args: AliasExpr) -> 'Query':
        return Query([With(args)])
