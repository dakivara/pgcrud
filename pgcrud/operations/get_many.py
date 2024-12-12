from typing import Any, Literal, TypeVar, overload

from psycopg import Cursor

from pgcrud.operations.shared import get_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, SelectValueType, FromValueType, WhereValueType, OrderByValueType, WindowValueType


T = TypeVar('T')


@overload
def get_many(
        cursor: Cursor[Any],
        as_: type[T],
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
) -> list[T]: ...


@overload
def get_many(
        cursor: Cursor[Any],
        as_: type[T],
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
) -> Cursor[T]: ...


def get_many(
        cursor: Cursor[Any],
        as_: type[T],
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
) -> list[T] | Cursor[T]:

    cursor.row_factory = get_row_factory(as_)
    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, limit, offset)
    cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        return cursor.fetchall()
