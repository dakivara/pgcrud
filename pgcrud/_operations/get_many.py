from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
def get_many(cursor: Cursor, select: str | Col, from_: TableType, *, where: WhereType | None = None, order_by: OrderByType | None = None, limit: int | None = None, offset: int | None = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def get_many(cursor: Cursor, select: Sequence[str | Col], from_: TableType, *, where: WhereType | None = None, order_by: OrderByType | None = None, limit: int | None = None, offset: int | None = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def get_many(cursor: Cursor, select: type[PydanticModel], from_: TableType, *, where: WhereType | None = None, order_by: OrderByType | None = None, limit: int | None = None, offset: int | None = None, no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
def get_many(cursor: Cursor, select: SelectType, from_: TableType, *, where: WhereType | None = None, order_by: OrderByType | None = None, limit: int | None = None, offset: int | None = None, no_fetch: Literal[True]) -> None: ...


def get_many(
        cursor: Cursor,
        select: SelectType,
        from_: TableType,
        *,
        where: WhereType | None = None,
        order_by: OrderByType | None = None,
        limit: int | None = None,
        offset: int | None = None,
        no_fetch: bool | None = False,
) -> list[ReturnType] | None:

    cursor.row_factory = get_row_factory(select)
    query = prepare_select_query(select, from_, where, order_by, limit, offset)
    cursor.execute(query)

    if not no_fetch:
        return cursor.fetchall()
