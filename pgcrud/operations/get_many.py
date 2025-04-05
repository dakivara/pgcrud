from collections.abc import Sequence
from typing import Any, Literal, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.operations.shared import construct_composed_get_query
from pgcrud.types import Row


@overload
def get_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        select: Any | Sequence[Any],
        from_: Any,
        *,
        where: Any | None = None,
        group_by: Any | Sequence[Any] | None = None,
        having: Any | None = None,
        window: Any | Sequence[Any] | None = None,
        order_by: Any | Sequence[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
def get_many(
        cursor: Cursor[Row],
        select: Any | Sequence[Any],
        from_: Any,
        *,
        where: Any | None = None,
        group_by: Any | Sequence[Any] | None = None,
        having: Any | None = None,
        window: Any | Sequence[Any] | None = None,
        order_by: Any | Sequence[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[True],
) -> Cursor[Row]: ...


@overload
def get_many(
        cursor: ServerCursor[Row],
        select: Any | Sequence[Any],
        from_: Any,
        *,
        where: Any | None = None,
        group_by: Any | Sequence[Any] | None = None,
        having: Any | None = None,
        window: Any | Sequence[Any] | None = None,
        order_by: Any | Sequence[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[True],
) -> ServerCursor[Row]: ...


def get_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        select: Any | Sequence[Any],
        from_: Any,
        *,
        where: Any | None = None,
        group_by: Any | Sequence[Any] | None = None,
        having: Any | None = None,
        window: Any | Sequence[Any] | None = None,
        order_by: Any | Sequence[Any] | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: bool | None = False,
) -> list[Row] | Cursor[Row] | ServerCursor[Row]:

    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, limit, offset)
    cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        return cursor.fetchall()
