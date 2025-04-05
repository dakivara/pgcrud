from collections.abc import Sequence
from typing import Any, Literal, overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_get_query
from pgcrud.types import Row


@overload
async def async_get_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
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
async def async_get_many(
        cursor: AsyncCursor[Row],
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
) -> AsyncCursor[Row]: ...


@overload
async def async_get_many(
        cursor: AsyncServerCursor[Row],
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
) -> AsyncServerCursor[Row]: ...


async def async_get_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
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
) -> list[Row] | AsyncCursor[Row] | AsyncServerCursor[Row]:

    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, limit, offset)
    await cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        return await cursor.fetchall()
