from collections.abc import Sequence
from typing import Any

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_get_query
from pgcrud.types import Row


async def async_get_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        select: Any | Sequence[Any],
        from_: Any,
        *,
        where: Any | None = None,
        group_by: Any | Sequence[Any] | None = None,
        having: Any | None = None,
        window: Any | Sequence[Any] | None = None,
        order_by: Any | Sequence[Any] | None = None,
        offset: int | None = None,
) -> Row | None:

    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, 1, offset)
    await cursor.execute(query)

    return await cursor.fetchone()
