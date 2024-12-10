from typing import Literal, TypeVar, overload

from psycopg import AsyncCursor

from pgcrud.operations.shared import get_async_row_factory, construct_composed_delete_query
from pgcrud.types import DeleteFromValueType, ReturningValueType, UsingValueType, WhereValueType


T = TypeVar('T')


@overload
async def delete_many(
        cursor: AsyncCursor[T],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def delete_many(
        cursor: AsyncCursor[T],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
async def delete_many(
        cursor: AsyncCursor[T],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        no_fetch: Literal[True],
) -> AsyncCursor[T]: ...


async def delete_many(
        cursor: AsyncCursor[T],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> list[T] | AsyncCursor[T] | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = construct_composed_delete_query(delete_from, using, where, returning)
    await cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
