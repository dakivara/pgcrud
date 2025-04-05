from __future__ import annotations

from typing import Any, Literal

from pgcrud.expressions.base import make_expr
from pgcrud.expressions.functions import (
    CryptFunctionExpression,
    GenSaltFunctionExpression,
    JsonBuildObjectFunctionExpression,
    LowerFunctionExpression,
    ToJsonFunctionExpression,
    UpperFunctionExpression,
    ArrayAggFunctionExpression,
    AvgFunctionExpression,
    MaxFunctionExpression,
    MinFunctionExpression,
    NowFunctionExpression,
    RowNumberFunctionExpression,
    CountFunctionExpression,
    JsonAggFunctionExpression,
    SumFunctionExpression,
    CoalesceFunctionExpression,
    CastFunctionExpression,
)


__all__ = [
    'row_number',
    'count',
    'sum',
    'avg',
    'min',
    'max',
    'lower',
    'upper',
    'array_agg',
    'json_agg',
    'coalesce',
    'to_json',
    'json_build_object',

    'crypt',
    'gen_salt',
]


def now() -> NowFunctionExpression:
    return NowFunctionExpression()


def row_number() -> RowNumberFunctionExpression:
    return RowNumberFunctionExpression()


def count(value: Any) -> CountFunctionExpression:
    return CountFunctionExpression(make_expr(value))


def sum(value: Any) -> SumFunctionExpression:
    return SumFunctionExpression(make_expr(value))


def avg(value: Any) -> AvgFunctionExpression:
    return AvgFunctionExpression(make_expr(value))


def min(value: Any) -> MinFunctionExpression:
    return MinFunctionExpression(make_expr(value))


def max(value: Any) -> MaxFunctionExpression:
    return MaxFunctionExpression(make_expr(value))


def lower(value: Any) -> LowerFunctionExpression:
    return LowerFunctionExpression(make_expr(value))


def upper(value: Any) -> UpperFunctionExpression:
    return UpperFunctionExpression(make_expr(value))


def array_agg(value: Any) -> ArrayAggFunctionExpression:
    return ArrayAggFunctionExpression(make_expr(value))


def json_agg(value: Any) -> JsonAggFunctionExpression:
    return JsonAggFunctionExpression(make_expr(value))


def coalesce(*args: Any) -> CoalesceFunctionExpression:
    return CoalesceFunctionExpression([make_expr(arg) for arg in args])


def to_json(value: Any) -> ToJsonFunctionExpression:
    return ToJsonFunctionExpression(make_expr(value))


def json_build_object(*args: Any) -> JsonBuildObjectFunctionExpression:
    return JsonBuildObjectFunctionExpression([make_expr(arg) for arg in args])


def cast(value: Any) -> CastFunctionExpression:
    return CastFunctionExpression(make_expr(value))


# pgcrypto extension


def crypt(
        password: Any,
        salt: Any,
) -> CryptFunctionExpression:
    return CryptFunctionExpression(make_expr(password), make_expr(salt))


def gen_salt(
        algorithm: Literal['bf', 'md5', 'sha256'],
        cost: int | None = None,
) -> GenSaltFunctionExpression:
    return GenSaltFunctionExpression(algorithm, cost)
