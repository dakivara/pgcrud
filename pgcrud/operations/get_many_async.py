from typing import Literal, overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, Row, SelectValueType, FromValueType, WhereValueType, OrderByValueType, WindowValueType


@overload
async def get_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        select: SelectValueType,
        from_: FromValueType,
        *,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        window: WindowValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
async def get_many(
        cursor: AsyncCursor[Row],
        select: SelectValueType,
        from_: FromValueType,
        *,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        window: WindowValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor[Row]: ...


@overload
async def get_many(
        cursor: AsyncServerCursor[Row],
        select: SelectValueType,
        from_: FromValueType,
        *,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        window: WindowValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[True],
) -> AsyncServerCursor[Row]: ...


async def get_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        select: SelectValueType,
        from_: FromValueType,
        *,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        window: WindowValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: bool | None = False,
) -> list[Row] | AsyncCursor[Row] | AsyncServerCursor[Row]:

    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, limit, offset)
    await cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        return await cursor.fetchall()
