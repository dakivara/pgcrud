from typing import Any, overload

from psycopg import Cursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
def get_one(cursor: Cursor, select: str, from_: str, *, where: WhereType = None, order_by: OrderByType = None, offset: int = None) -> Any | None: ...


@overload
def get_one(cursor: Cursor, select: tuple[str] | _TSTAR, from_: str, *, where: WhereType = None, order_by: OrderByType = None, offset: int = None) -> tuple[Any, ...] | None: ...


@overload
def get_one(cursor: Cursor, select: list[str] | _DSTAR, from_: str, *, where: WhereType = None, order_by: OrderByType = None, offset: int = None) -> dict[str, Any] | None: ...


@overload
def get_one(cursor: Cursor, select: type[OutputModel], from_: str, *, where: WhereType = None, order_by: OrderByType = None, offset: int = None) -> OutputModel | None: ...


def get_one(
        cursor: Cursor,
        select: SelectType,
        from_: str,
        *,
        where: WhereType = None,
        order_by: OrderByType = None,
        offset: int = None,
) -> ReturnType | None:

    cursor.row_factory = get_row_factory(select)
    query = prepare_select_query(select, from_, where, order_by, 1, offset)
    cursor.execute(query)

    return cursor.fetchone()
