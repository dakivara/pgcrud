from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
async def update_many(cursor: AsyncCursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: Literal[None] = None, exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> None: ...


@overload
async def update_many(cursor: AsyncCursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: str | Col, exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
async def update_many(cursor: AsyncCursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: Sequence[str | Col], exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
async def update_many(cursor: AsyncCursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: type[PydanticModel], exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
async def update_many(cursor: AsyncCursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: SelectType | None = None, exclude: ExcludeType | None = None, no_fetch: Literal[True]) -> None: ...


async def update_many(
        cursor: AsyncCursor,
        update: TableType,
        set_: SetType,
        *,
        where: WhereType | None = None,
        returning: SelectType | None = None,
        exclude: ExcludeType | None = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = prepare_update_query(update, set_, where, returning, exclude)
    await cursor.execute(query)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
