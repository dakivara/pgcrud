from collections.abc import Sequence
from typing import Any, Literal, overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_delete_query
from pgcrud.types import Row


@overload
async def async_delete_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def async_delete_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
async def async_delete_many(
        cursor: AsyncCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        no_fetch: Literal[True],
) -> AsyncCursor[Row]: ...


@overload
async def async_delete_many(
        cursor: AsyncServerCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        no_fetch: Literal[True],
) -> AsyncServerCursor[Row]: ...


async def async_delete_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any] | None = None,
        no_fetch: bool = False,
) -> list[Row] | AsyncCursor[Row] | AsyncServerCursor[Row] | None:

    query = construct_composed_delete_query(delete_from, using, where, returning)
    await cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
