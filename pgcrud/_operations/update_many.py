from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
def update_many(cursor: Cursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: Literal[None] = None, exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> None: ...


@overload
def update_many(cursor: Cursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: str | Col, exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def update_many(cursor: Cursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: Sequence[str | Col], exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def update_many(cursor: Cursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: type[PydanticModel], exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
def update_many(cursor: Cursor, update: TableType, set_: SetType, *, where: WhereType | None = None, returning: SelectType | None = None, exclude: ExcludeType | None = None, no_fetch: Literal[True]) -> None: ...


def update_many(
        cursor: Cursor,
        update: TableType,
        set_: SetType,
        *,
        where: WhereType | None = None,
        returning: SelectType | None = None,
        exclude: ExcludeType | None = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = prepare_update_query(update, set_, where, returning, exclude)
    cursor.execute(query)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
