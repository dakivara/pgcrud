from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor
from psycopg.abc import Query

from pgcrud.col import Col
from pgcrud.operations.type_hints import *
from pgcrud.operations.utils import *


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType | None = None, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType | None = None, returning: str | Col, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType | None = None, returning: Sequence[str | Col], no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType | None = None, returning: type[PydanticModel], no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType | None = None, returning: SelectType | None = None, no_fetch: Literal[True]) -> None: ...


def execute(
        cursor: Cursor,
        query: Query,
        *,
        params: ParamsType | None = None,
        returning: SelectType | None = None,
        no_fetch: bool = False,
) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_execute_params(params)
    cursor.execute(query, params)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
