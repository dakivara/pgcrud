from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
async def get_many(cursor: AsyncCursor, select: str, from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
async def get_many(cursor: AsyncCursor, select: tuple[str] | _TSTAR, from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
async def get_many(cursor: AsyncCursor, select: list[str] | _DSTAR, from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[False] = False) -> list[dict[str, Any]]: ...


@overload
async def get_many(cursor: AsyncCursor, select: type[OutputModel], from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[False] = False) -> list[OutputModel]: ...


@overload
async def get_many(cursor: AsyncCursor, select: SelectType, from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[True] = False) -> None: ...


async def get_many(
        cursor: AsyncCursor,
        select: SelectType,
        from_: str,
        *,
        where: WhereType = None,
        order_by: OrderByType = None,
        limit: int = None,
        offset: int = None,
        no_fetch: bool = False,
) -> list[ReturnType]:

    cursor.row_factory = get_row_factory(select)
    query = prepare_select_query(select, from_, where, order_by, limit, offset)
    await cursor.execute(query)

    if not no_fetch:
        return await cursor.fetchall()
