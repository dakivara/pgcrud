from typing import Any

from pgcrud.expr import ArrayAggExpr, CountExpr, make_expr, Expr, AvgExpr, SumExpr, ToJsonExpr, JsonAggExpr, CoalesceExpr, MinExpr, MaxExpr, RowNumberExpr


__all__ = [
    'count',
    'sum',
    'avg',
    'min',
    'max',
    'array_agg',
    'json_agg',
    'coalesce',
    'to_json',
    'row_number',
]


def count(expr: Expr) -> CountExpr:
    return CountExpr(expr)


def sum(expr: Expr) -> SumExpr:
    return SumExpr(expr)


def avg(expr: Expr) -> AvgExpr:
    return AvgExpr(expr)


def min(expr: Expr) -> MinExpr:
    return MinExpr(expr)


def max(expr: Expr) -> MaxExpr:
    return MaxExpr(expr)


def array_agg(expr: Expr) -> ArrayAggExpr:
    return ArrayAggExpr(expr)


def json_agg(expr: Expr) -> JsonAggExpr:
    return JsonAggExpr(expr)


def coalesce(*args: Any) -> CoalesceExpr:
    return CoalesceExpr([make_expr(arg) for arg in args])


def to_json(expr: Expr) -> ToJsonExpr:
    return ToJsonExpr(expr)


def row_number() -> RowNumberExpr:
    return RowNumberExpr()
