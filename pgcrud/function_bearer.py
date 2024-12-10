from typing import Any

from pgcrud.expr import ArrayAggExpr, CountExpr, make_expr, Expr, AvgExpr, SumExpr, ToJsonExpr, JsonAggExpr, CoalesceExpr, MinExpr, MaxExpr

__all__ = ['FunctionBearer']


class FunctionBearer:

    def __new__(cls):
        raise TypeError("'FunctionBearer' object is not callable")

    @staticmethod
    def count(expr: Expr) -> CountExpr:
        return CountExpr(expr)

    @staticmethod
    def sum(expr: Expr) -> SumExpr:
        return SumExpr(expr)

    @staticmethod
    def avg(expr: Expr) -> AvgExpr:
        return AvgExpr(expr)

    @staticmethod
    def min(expr: Expr) -> MinExpr:
        return MinExpr(expr)

    @staticmethod
    def max(expr: Expr) -> MaxExpr:
        return MaxExpr(expr)

    @staticmethod
    def array_agg(expr: Expr) -> ArrayAggExpr:
        return ArrayAggExpr(expr)

    @staticmethod
    def json_agg(expr: Expr) -> JsonAggExpr:
        return JsonAggExpr(expr)

    @staticmethod
    def coalesce(*args: Any) -> CoalesceExpr:
        return CoalesceExpr([make_expr(arg) for arg in args])

    @staticmethod
    def to_json(expr: Expr) -> ToJsonExpr:
        return ToJsonExpr(expr)
