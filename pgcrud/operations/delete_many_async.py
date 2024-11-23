from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud.col import Col
from pgcrud.operations.type_hints import *
from pgcrud.operations.utils import *


@overload
async def delete_many(cursor: AsyncCursor, delete_from: TableType, *, where: WhereType | None = None, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
async def delete_many(cursor: AsyncCursor, delete_from: TableType, *, where: WhereType | None = None, returning: Col, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
async def delete_many(cursor: AsyncCursor, delete_from: TableType, *, where: WhereType | None = None, returning: tuple[Col, ...], no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
async def delete_many(cursor: AsyncCursor, delete_from: TableType, *, where: WhereType | None = None, returning: type[PydanticModel], no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
async def delete_many(cursor: AsyncCursor, delete_from: TableType, *, where: WhereType | None = None, returning: SelectType | None = None, no_fetch: Literal[True]) -> None: ...


async def delete_many(
        cursor: AsyncCursor,
        delete_from: TableType,
        *,
        where: WhereType | None = None,
        returning: SelectType | None = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = prepare_delete_query(delete_from, where, returning)
    await cursor.execute(query)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
