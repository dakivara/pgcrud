from __future__ import annotations

from typing import Any, TYPE_CHECKING

from pgcrud.expressions import (
    ToJson,
    make_expr,
    ArrayAgg,
    Avg,
    Expression,
    Max,
    Min,
    RowNumber,
    Count,
    JsonAgg,
    Sum,
    Coalesce,
)

if TYPE_CHECKING:
    from pgcrud.query import Query


__all__ = [
    'row_number',
    'count',
    'sum',
    'avg',
    'min',
    'max',
    'array_agg',
    'json_agg',
    'coalesce',
    'to_json',
]


def row_number() -> RowNumber:
    return RowNumber()


def count(value: Any | Expression | Query) -> Count:
    return Count(make_expr(value))


def sum(value: Any | Expression | Query) -> Sum:
    return Sum(make_expr(value))


def avg(value: Any | Expression | Query) -> Avg:
    return Avg(make_expr(value))


def min(value: Any | Expression | Query) -> Min:
    return Min(make_expr(value))


def max(value: Any | Expression | Query) -> Max:
    return Max(make_expr(value))


def array_agg(value: Any | Expression | Query) -> ArrayAgg:
    return ArrayAgg(make_expr(value))


def json_agg(value: Any | Expression | Query) -> JsonAgg:
    return JsonAgg(make_expr(value))


def coalesce(*args: Any | Expression | Query) -> Coalesce:
    return Coalesce([make_expr(arg) for arg in args])


def to_json(value: Any | Expression | Query) -> ToJson:
    return ToJson(make_expr(value))
