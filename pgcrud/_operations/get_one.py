from collections.abc import Sequence
from typing import Any, overload

from psycopg import Cursor

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
def get_one(
        cursor: Cursor,
        select: str | Col,
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        offset: int | None = None,
) -> Any | None: ...


@overload
def get_one(
        cursor: Cursor,
        select: Sequence[str | Col],
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        offset: int | None = None,
) -> tuple[Any, ...] | None: ...


@overload
def get_one(
        cursor: Cursor,
        select: type[PydanticModel],
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        offset: int | None = None,
) -> PydanticModel | None: ...


def get_one(
        cursor: Cursor,
        select: SelectType,
        from_: TableType,
        *,
        join: JoinType | None = None,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        offset: int | None = None,
) -> ReturnType | None:

    cursor.row_factory = get_row_factory(select)
    query = prepare_select_query(select, from_, join, where, order_by, 1, offset)
    cursor.execute(query)

    return cursor.fetchone()
