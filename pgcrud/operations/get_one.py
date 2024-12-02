from collections.abc import Sequence
from typing import Any, overload

from psycopg import Cursor

from pgcrud.expr import Expr
from pgcrud.operations.shared import get_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, HavingValueType, PydanticModel, SelectValueType, FromValueType, WhereValueType, OrderByValueType, ResultOneValueType


@overload
def get_one(
        cursor: Cursor,
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
def get_one(
        cursor: Cursor,
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
def get_one(
        cursor: Cursor,
        select: type[PydanticModel],
        from_: FromValueType,
        *,
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
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        having: HavingValueType | None = None,
        order_by: OrderByValueType | None = None,
        offset: int | None = None,
) -> ResultOneValueType | None:

    cursor.row_factory = get_row_factory(select)
    query = construct_composed_get_query(select, from_, where, group_by, having, order_by, 1, offset)
    cursor.execute(query)

    return cursor.fetchone()
