from collections.abc import Sequence
from typing import Any, overload

from psycopg import Cursor

from pgcrud.col import Col
from pgcrud.operations.shared import get_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, PydanticModel, SelectValueType, FromValueType, WhereValueType, JoinValueType, OrderByValueType, ResultOneValueType


@overload
def get_one(
        cursor: Cursor,
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
def get_one(
        cursor: Cursor,
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
def get_one(
        cursor: Cursor,
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


def get_one(
        cursor: Cursor,
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

    cursor.row_factory = get_row_factory(select)
    query = construct_composed_get_query(select, from_, join, where, group_by, having, order_by, 1, offset)
    cursor.execute(query)

    return cursor.fetchone()
