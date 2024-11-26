from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud.col import Col
from pgcrud.operations.utils import get_row_factory, construct_composed_get_query
from pgcrud.types import GroupByValueType, PydanticModel, SelectValueType, FromValueType, JoinValueType, WhereValueType, OrderByValueType, ResultManyValueType


@overload
def get_many(
        cursor: Cursor,
        select: Col,
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
def get_many(
        cursor: Cursor,
        select: Sequence[Col],
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
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
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
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
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: Literal[True],
) -> None: ...


def get_many(
        cursor: Cursor,
        select: SelectValueType,
        from_: FromValueType,
        *,
        join: JoinValueType | None = None,
        where: WhereValueType | None = None,
        group_by: GroupByValueType | None = None,
        order_by: OrderByValueType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: bool | None = False,
) -> ResultManyValueType | None:

    cursor.row_factory = get_row_factory(select)
    query = construct_composed_get_query(select, from_, join, where, group_by, order_by, limit, offset)
    cursor.execute(query)

    if not no_fetch:
        return cursor.fetchall()
