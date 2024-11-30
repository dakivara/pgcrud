from typing import Any

from pgcrud.expr import make_expr, Expr, UndefinedExpr, AvgExpr, SumExpr, ToJsonExpr, JsonAggExpr, CoalesceExpr


__all__ = ['FunctionBearer']


class FunctionBearer:

    def __new__(cls):
        raise TypeError("'FunctionBearer' object is not callable")

    @staticmethod
    def sum(expr: Expr) -> SumExpr | UndefinedExpr:
        if expr:
            return SumExpr(expr)
        else:
            return UndefinedExpr()

    @staticmethod
    def avg(expr: Expr) -> AvgExpr | UndefinedExpr:
        if expr:
            return AvgExpr(expr)
        else:
            return UndefinedExpr()

    @staticmethod
    def json_agg(expr: Expr) -> JsonAggExpr | UndefinedExpr:
        if expr:
            return JsonAggExpr(expr)
        else:
            return UndefinedExpr()

    @staticmethod
    def coalesce(*args: Any) -> CoalesceExpr | UndefinedExpr:
        exprs = []

        for arg in args:
            expr = make_expr(arg)
            if expr:
                exprs.append(expr)

        if exprs:
            return CoalesceExpr(exprs)
        else:
            return UndefinedExpr()

    @staticmethod
    def to_json(expr: Expr) -> ToJsonExpr | UndefinedExpr:
        if expr:
            return ToJsonExpr(expr)
        else:
            return UndefinedExpr()
