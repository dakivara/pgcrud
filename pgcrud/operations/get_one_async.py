from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, Row, SelectValueType, FromValueType, WhereValueType, OrderByValueType, WindowValueType


async def get_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        select: SelectValueType,
        from_: FromValueType,
        *,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        window: WindowValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> Row | None:

    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, 1, offset)
    await cursor.execute(query)

    return await cursor.fetchone()
