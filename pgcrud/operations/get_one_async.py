from collections.abc import Sequence
from typing import Any, overload

from psycopg import AsyncCursor

from pgcrud.col import Col
from pgcrud.operations.shared import get_async_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, PydanticModel, SelectValueType, FromValueType, WhereValueType, JoinValueType, OrderByValueType, ResultOneValueType


@overload
async def get_one(
        cursor: AsyncCursor,
        select: Col,
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> Any | None: ...


@overload
async def get_one(
        cursor: AsyncCursor,
        select: Sequence[Col],
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> tuple[Any, ...] | None: ...


@overload
async def get_one(
        cursor: AsyncCursor,
        select: type[PydanticModel],
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> PydanticModel | None: ...


async def get_one(
        cursor: AsyncCursor,
        select: SelectValueType,
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> ResultOneValueType | None:

    cursor.row_factory = get_async_row_factory(select)
    query = construct_composed_get_query(select, from_, join, where, group_by, having, order_by, 1, offset)
    await cursor.execute(query)

    return await cursor.fetchone()
