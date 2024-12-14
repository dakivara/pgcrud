from typing import Literal, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.operations.shared import construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, Row, SelectValueType, FromValueType, WhereValueType, OrderByValueType, WindowValueType


@overload
def get_many(
        cursor: Cursor[Row] | ServerCursor[Row],
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
def get_many(
        cursor: Cursor[Row],
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
) -> Cursor[Row]: ...


@overload
def get_many(
        cursor: ServerCursor[Row],
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
) -> ServerCursor[Row]: ...


def get_many(
        cursor: Cursor[Row] | ServerCursor[Row],
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
) -> list[Row] | Cursor[Row] | ServerCursor[Row]:

    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, limit, offset)
    cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        return cursor.fetchall()
