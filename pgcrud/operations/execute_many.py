from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor
from psycopg.abc import Query

from pgcrud.col import Col
from pgcrud.operations.utils import get_row_factory, prepare_execute_many_params
from pgcrud.types import PydanticModel, ParamsValueType, ResultManyValueType, ReturningValueType


@overload
def execute_many(
        cursor: Cursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: Literal[None] = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def execute_many(
        cursor: Cursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: Col,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
def execute_many(
        cursor: Cursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: Sequence[Col],
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
def execute_many(
        cursor: Cursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: type[PydanticModel],
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
def execute_many(
        cursor: Cursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: ReturningValueType | None = None,
        no_fetch: Literal[True],
) -> None: ...


def execute_many(
        cursor: Cursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_execute_many_params(params)
    cursor.executemany(query, params, returning=True if returning else False)

    if not no_fetch:
        if returning:
            rows = []

            while True:
                rows += cursor.fetchall()
                if not cursor.nextset():
                    break

            return rows
