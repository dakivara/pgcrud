from collections.abc import Sequence
from typing import Any, overload

from psycopg import AsyncCursor

from pgcrud.expr import Expr
from pgcrud.operations.shared import get_async_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, PydanticModel, SelectValueType, FromValueType, WhereValueType, OrderByValueType, ResultOneValueType


@overload
async def get_one(
        cursor: AsyncCursor,
        select: Expr,
        from_: FromValueType,
        *,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> Any | None: ...


@overload
async def get_one(
        cursor: AsyncCursor,
        select: Sequence[Expr],
        from_: FromValueType,
        *,
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
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> ResultOneValueType | None:

    cursor.row_factory = get_async_row_factory(select)
    query = construct_composed_get_query(select, from_, where, group_by, having, order_by, 1, offset)
    await cursor.execute(query)

    return await cursor.fetchone()
