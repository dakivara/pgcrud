from typing import Any, TypeVar

from psycopg import AsyncCursor

from pgcrud.operations.shared import get_async_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, SelectValueType, FromValueType, WhereValueType, OrderByValueType, WindowValueType


T = TypeVar('T')


async def get_one(
        cursor: AsyncCursor[Any],
        as_: type[T],
        select: SelectValueType,
        from_: FromValueType,
        *,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        window: WindowValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> T | None:

    cursor.row_factory = get_async_row_factory(as_)
    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, 1, offset)
    await cursor.execute(query)

    return await cursor.fetchone()
