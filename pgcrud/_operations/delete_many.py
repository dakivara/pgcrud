from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
def delete_many(cursor: Cursor, delete_from: TableType, *, where: WhereType | None = None, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
def delete_many(cursor: Cursor, delete_from: TableType, *, where: WhereType | None = None, returning: str | Col, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def delete_many(cursor: Cursor, delete_from: TableType, *, where: WhereType | None = None, returning: Sequence[str | Col], no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def delete_many(cursor: Cursor, delete_from: TableType, *, where: WhereType | None = None, returning: type[PydanticModel], no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
def delete_many(cursor: Cursor, delete_from: TableType, *, where: WhereType | None = None, returning: SelectType | None = None, no_fetch: Literal[True]) -> None: ...


def delete_many(
        cursor: Cursor,
        delete_from: TableType,
        *,
        where: WhereType | None = None,
        returning: SelectType | None = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = prepare_delete_query(delete_from, where, returning)
    cursor.execute(query)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
