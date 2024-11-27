from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud.col import Col
from pgcrud.operations.utils import get_async_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, PydanticModel, SelectValueType, FromValueType, JoinValueType, WhereValueType, OrderByValueType, ResultManyValueType


@overload
async def get_many(
        cursor: AsyncCursor,
        select: Col,
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
async def get_many(
        cursor: AsyncCursor,
        select: Sequence[Col],
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
async def get_many(
        cursor: AsyncCursor,
        select: type[PydanticModel],
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
async def get_many(
        cursor: AsyncCursor,
        select: SelectValueType,
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[True],
) -> None: ...


async def get_many(
        cursor: AsyncCursor,
        select: SelectValueType,
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: bool | None = False,
) -> ResultManyValueType | None:

    cursor.row_factory = get_async_row_factory(select)
    query = construct_composed_get_query(select, from_, join, where, group_by, having, order_by, limit, offset)
    await cursor.execute(query)

    if not no_fetch:
        return await cursor.fetchall()
