from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
async def update_many(cursor: AsyncCursor, update: str, set_: SetType, *, where: WhereType = None, returning: Literal[None] = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> None: ...


@overload
async def update_many(cursor: AsyncCursor, update: str, set_: SetType, *, where: WhereType = None, returning: str = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[Any]: ...


@overload
async def update_many(cursor: AsyncCursor, update: str, set_: SetType, *, where: WhereType = None, returning: tuple[str, ...] | _TSTAR = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[tuple[Any, ...]]: ...


@overload
async def update_many(cursor: AsyncCursor, update: str, set_: SetType, *, where: WhereType = None, returning: list[str] | _DSTAR = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[dict[str, Any]]: ...


@overload
async def update_many(cursor: AsyncCursor, update: str, set_: SetType, *, where: WhereType = None, returning: type[OutputModel] = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[OutputModel]: ...


@overload
async def update_many(cursor: AsyncCursor, update: str, set_: SetType, *, where: WhereType = None, returning: SelectType = None, exclude: ExcludeType = None, no_fetch: Literal[True] = False, **kwargs) -> None: ...


async def update_many(
        cursor: AsyncCursor,
        update: str,
        set_: SetType,
        *,
        where: WhereType = None,
        returning: SelectType = None,
        exclude: ExcludeType = None,
        no_fetch: bool = False,
        **kwargs,
) -> list[ReturnType] | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = prepare_update_query(update, set_, where, returning, exclude, kwargs)
    await cursor.execute(query)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
