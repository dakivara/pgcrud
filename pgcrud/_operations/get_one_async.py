from typing import Any, overload

from psycopg import AsyncCursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
async def get_one(cursor: AsyncCursor, select: str, from_: str, *, where: WhereType = None, order_by: OrderByType = None, offset: int = None) -> Any | None: ...


@overload
async def get_one(cursor: AsyncCursor, select: tuple[str] | _TSTAR, from_: str, *, where: WhereType = None, order_by: OrderByType = None, offset: int = None) -> tuple[Any, ...] | None: ...


@overload
async def get_one(cursor: AsyncCursor, select: list[str] | _DSTAR, from_: str, *, where: WhereType = None, order_by: OrderByType = None, offset: int = None) -> dict[str, Any] | None: ...


@overload
async def get_one(cursor: AsyncCursor, select: type[OutputModel], from_: str, *, where: WhereType = None, order_by: OrderByType = None, offset: int = None) -> OutputModel | None: ...


async def get_one(
        cursor: AsyncCursor,
        select: SelectType,
        from_: str,
        *,
        where: WhereType = None,
        order_by: OrderByType = None,
        offset: int = None,
) -> ReturnType | None:

    cursor.row_factory = get_row_factory(select)
    query = prepare_select_query(select, from_, where, order_by, 1, offset)
    await cursor.execute(query)

    return await cursor.fetchone()
