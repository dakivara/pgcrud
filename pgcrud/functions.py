from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

from pgcrud.expressions import (
    Crypt,
    GenSalt,
    Lower,
    ToJson,
    Upper,
    make_expr,
    ArrayAgg,
    Avg,
    Expression,
    Max,
    Min,
    Now,
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
    'lower',
    'upper',
    'array_agg',
    'json_agg',
    'coalesce',
    'to_json',

    'crypt',
    'gen_salt',
]


def now() -> Now:
    return Now()


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


def lower(value: Any | Expression | Query) -> Lower:
    return Lower(make_expr(value))


def upper(value: Any | Expression | Query) -> Upper:
    return Upper(make_expr(value))


def array_agg(value: Any | Expression | Query) -> ArrayAgg:
    return ArrayAgg(make_expr(value))


def json_agg(value: Any | Expression | Query) -> JsonAgg:
    return JsonAgg(make_expr(value))


def coalesce(*args: Any | Expression | Query) -> Coalesce:
    return Coalesce([make_expr(arg) for arg in args])


def to_json(value: Any | Expression | Query) -> ToJson:
    return ToJson(make_expr(value))


# pgcrypto extension


def crypt(
        password: str | Expression,
        salt: str | Expression,
) -> Crypt:
    return Crypt(make_expr(password), make_expr(salt))


def gen_salt(
        algorithm: Literal['bf', 'md5', 'sha256'],
        cost: int | None = None,
) -> GenSalt:
    return GenSalt(algorithm, cost)
