from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor
from psycopg.abc import Query

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
def execute_many(cursor: Cursor, query: Query, params: Sequence[ParamsType], *, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
def execute_many(cursor: Cursor, query: Query, params: Sequence[ParamsType], *, returning: str | Col, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def execute_many(cursor: Cursor, query: Query, params: Sequence[ParamsType], *, returning: Sequence[str | Col], no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def execute_many(cursor: Cursor, query: Query, params: Sequence[ParamsType], *, returning: type[PydanticModel], no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
def execute_many(cursor: Cursor, query: Query,params: Sequence[ParamsType], *, returning: SelectType | None = None, no_fetch: Literal[True]) -> None: ...


def execute_many(
        cursor: Cursor,
        query: Query,
        params: Sequence[ParamsType],
        *,
        returning: SelectType | None = None,
        no_fetch: bool = False,
) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_execute_params_seq(params)
    cursor.executemany(query, params, returning=True if returning else False)

    if not no_fetch:
        if returning:
            rows = []

            while True:
                rows.append(cursor.fetchone())
                if not cursor.nextset():
                    break

            return rows
