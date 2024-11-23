from typing import Any, Literal, Sequence, overload

from psycopg import AsyncCursor

from pgcrud.col import Col
from pgcrud.operations.type_hints import *
from pgcrud.operations.utils import *


@overload
async def get_many(
        cursor: AsyncCursor,
        select: str | Col,
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
async def get_many(
        cursor: AsyncCursor,
        select: Sequence[str | Col],
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
async def get_many(
        cursor: AsyncCursor,
        select: type[PydanticModel],
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
async def get_many(
        cursor: AsyncCursor,
        select: SelectType,
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[True],
) -> None: ...


async def get_many(
        cursor: AsyncCursor,
        select: SelectType,
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:

    cursor.row_factory = get_async_row_factory(select)
    query = prepare_select_query(select, from_, join, where, order_by, limit, offset)
    await cursor.execute(query)

    if not no_fetch:
        return await cursor.fetchall()
