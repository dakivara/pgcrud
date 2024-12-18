from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from psycopg.sql import SQL, Composed

from pgcrud.clauses import Clause, DeleteFrom, From, Select, Values, Where, GroupBy, Having, OrderBy, Offset, Limit, InsertInto, Returning, Set, Update, Using, PartitionBy, RowsBetween, With, RangeBetween, Window
from pgcrud.expr import Expr, AliasExpr, QueryExpr, ReferenceExpr, TableReferenceExpr, make_expr
from pgcrud.frame_boundaries import FrameBoundary
from pgcrud.operators import FilterOperator, SortOperator
from pgcrud.utils import ensure_seq

if TYPE_CHECKING:
    from pgcrud.clauses import Clause


__all__ = ['Query']


@dataclass
class Query:
    clauses: list[Clause]

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return str(self)

    def get_composed(self) -> Composed:
        return SQL(' ').join([clause.get_composed() for clause in self.clauses if clause])

    def SELECT(self, *args: Any | Expr) -> 'Query':
        self.clauses.append(Select([make_expr(v) for v in args]))
        return self

    def FROM(self, value: Expr) -> 'Query':
        self.clauses.append(From(value))
        return self

    def WHERE(self, value: FilterOperator) -> 'Query':
        self.clauses.append(Where(value))
        return self

    def GROUP_BY(self, *args: Any | Expr) -> 'Query':
        self.clauses.append(GroupBy([make_expr(v) for v in args]))
        return self

    def HAVING(self, value: FilterOperator) -> 'Query':
        self.clauses.append(Having(value))
        return self

    def WINDOW(self, *args: AliasExpr) -> 'Query':
        self.clauses.append(Window(args))
        return self

    def ORDER_BY(self, *args: Any | Expr | SortOperator) -> 'Query':
        self.clauses.append(OrderBy([v if isinstance(v, (Expr, SortOperator)) else make_expr(v) for v in args]))
        return self

    def LIMIT(self, value: int) -> 'Query':
        self.clauses.append(Limit(value))
        return self

    def OFFSET(self, value: int) -> 'Query':
        self.clauses.append(Offset(value))
        return self

    def INSERT_INTO(self, value: TableReferenceExpr) -> 'Query':
        self.clauses.append(InsertInto(value))
        return self

    def VALUES(self, *args: Any | Sequence[Any] | dict[str, Any], **kwargs: Any) -> 'Query':
        prev_clause = self.clauses[-1] if len(self.clauses) > 0 and isinstance(self.clauses[-1], InsertInto) else None
        self.clauses.append(Values(args, kwargs, prev_clause))
        return self

    def RETURNING(self, *args: Any | Expr) -> 'Query':
        self.clauses.append(Returning([make_expr(v) for v in args]))
        return self

    def UPDATE(self, value: ReferenceExpr) -> 'Query':
        self.clauses.append(Update(value))
        return self

    def SET(self, cols: ReferenceExpr | Sequence[ReferenceExpr], values: Any | Sequence[Any] | dict[str, Any], **kwargs: Any) -> 'Query':
        self.clauses.append(Set(ensure_seq(cols), values, kwargs))
        return self

    def DELETE_FROM(self, value: ReferenceExpr) -> 'Query':
        self.clauses.append(DeleteFrom(value))
        return self

    def USING(self, value: Expr) -> 'Query':
        self.clauses.append(Using(value))
        return self

    def PARTITION_BY(self, *args: Expr) -> 'Query':
        self.clauses.append(PartitionBy(args))
        return self

    def ROWS_BETWEEN(self, start: FrameBoundary, end: FrameBoundary) -> 'Query':
        self.clauses.append(RowsBetween(start, end))
        return self

    def RANGE_BETWEEN(self, start: FrameBoundary, end: FrameBoundary) -> 'Query':
        self.clauses.append(RangeBetween(start, end))
        return self

    def WITH(self, *args: AliasExpr) -> 'Query':
        self.clauses.append(With(args))
        return self

    def AS(self, alias: str) -> AliasExpr:
        return QueryExpr(self).AS(alias)
