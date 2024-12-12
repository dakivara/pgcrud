from typing import Any, Literal, TypeVar, overload

from psycopg import AsyncCursor

from pgcrud.operations.shared import get_async_row_factory, construct_composed_delete_query
from pgcrud.types import DeleteFromValueType, ReturningValueType, UsingValueType, WhereValueType


T = TypeVar('T')


@overload
async def delete_many(
        cursor: AsyncCursor[Any],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def delete_many(
        cursor: AsyncCursor[Any],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        as_: type[T],
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
async def delete_many(
        cursor: AsyncCursor[Any],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        as_: type[T],
        no_fetch: Literal[True],
) -> AsyncCursor[T]: ...


async def delete_many(
        cursor: AsyncCursor[Any],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        as_: type[T] | None = None,
        no_fetch: bool = False,
) -> list[T] | AsyncCursor[T] | None:

    if returning and as_:
        cursor.row_factory = get_async_row_factory(as_)

    query = construct_composed_delete_query(delete_from, using, where, returning)
    await cursor.execute(query)

    if returning and as_:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
