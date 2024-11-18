from typing import Any, Literal, overload

from psycopg import Cursor
from psycopg.abc import Query

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType = None, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType = None, returning: str = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType = None, returning: tuple[str, ...] | _TSTAR = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType = None, returning: list[str] | _DSTAR = None, no_fetch: Literal[False] = False) -> list[dict[str, Any]]: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType = None, returning: type[OutputModel] = None, no_fetch: Literal[False] = False) -> list[OutputModel]: ...


@overload
def execute(cursor: Cursor, query: Query, *, params: ParamsType = None, returning: SelectType = None, no_fetch: Literal[True] = False) -> None: ...


def execute(
        cursor: Cursor,
        query: Query,
        *,
        params: ParamsType = None,
        returning: SelectType = None,
        no_fetch: bool = False,
) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_execute_params(params)
    cursor.execute(query, params)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
