from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud.expr import Expr
from pgcrud.operations.shared import get_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, PydanticModel, SelectValueType, FromValueType, WhereValueType, OrderByValueType, ResultManyValueType, WindowValueType


@overload
def get_many(
        cursor: Cursor,
        select: Expr,
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
) -> list[Any]: ...


@overload
def get_many(
        cursor: Cursor,
        select: Sequence[Expr],
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
) -> list[tuple[Any, ...]]: ...


@overload
def get_many(
        cursor: Cursor,
        select: type[PydanticModel],
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
) -> list[PydanticModel]: ...


@overload
def get_many(
        cursor: Cursor,
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
) -> Cursor: ...


def get_many(
        cursor: Cursor,
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
) -> ResultManyValueType | Cursor:

    cursor.row_factory = get_row_factory(select)
    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, limit, offset)
    cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        return cursor.fetchall()
