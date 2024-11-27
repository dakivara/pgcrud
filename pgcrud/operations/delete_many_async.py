from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud.col import Col
from pgcrud.operations.shared import get_async_row_factory, construct_composed_delete_query
from pgcrud.types import PydanticModel, DeleteFromValueType, ResultManyValueType, ReturningValueType, UsingValueType, WhereValueType


@overload
async def delete_many(
        cursor: AsyncCursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def delete_many(
        cursor: AsyncCursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: Col,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
async def delete_many(
        cursor: AsyncCursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: Sequence[Col],
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
async def delete_many(
        cursor: AsyncCursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: type[PydanticModel],
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
async def delete_many(
        cursor: AsyncCursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: Literal[True],
) -> None: ...


async def delete_many(
        cursor: AsyncCursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = construct_composed_delete_query(delete_from, using, where, returning)
    await cursor.execute(query)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
