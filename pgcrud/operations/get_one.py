from typing import TypeVar

from psycopg import Cursor

from pgcrud.operations.shared import get_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, SelectValueType, FromValueType, WhereValueType, OrderByValueType, WindowValueType


T = TypeVar('T')


def get_one(
        cursor: Cursor[T],
        select: SelectValueType,
        from_: FromValueType,
        *,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        window: WindowValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> T | None:

    cursor.row_factory = get_row_factory(select)
    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, 1, offset)
    cursor.execute(query)

    return cursor.fetchone()
