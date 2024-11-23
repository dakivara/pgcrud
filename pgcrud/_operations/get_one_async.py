from collections.abc import Sequence
from typing import Any, overload

from psycopg import AsyncCursor

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
async def get_one(cursor: AsyncCursor, select: str | Col, from_: TableType, *, where: WhereType | None = None, order_by: OrderByType | None = None, offset: int | None = None) -> Any | None: ...


@overload
async def get_one(cursor: AsyncCursor, select: Sequence[str | Col], from_: TableType, *, where: WhereType | None = None, order_by: OrderByType | None = None, offset: int | None = None) -> tuple[Any, ...] | None: ...


@overload
async def get_one(cursor: AsyncCursor, select: type[PydanticModel], from_: TableType, *, where: WhereType | None = None, order_by: OrderByType | None = None, offset: int | None = None) -> PydanticModel | None: ...


async def get_one(
        cursor: AsyncCursor,
        select: SelectType,
        from_: TableType,
        *,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        offset: int | None = None,
) -> ReturnType | None:

    cursor.row_factory = get_async_row_factory(select)
    query = prepare_select_query(select, from_, where, order_by, 1, offset)
    await cursor.execute(query)

    return await cursor.fetchone()
