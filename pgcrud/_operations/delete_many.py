from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
def delete_many(cursor: Cursor, delete_from: str, *, where: WhereType = None, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
def delete_many(cursor: Cursor, delete_from: str, *, where: WhereType = None, returning: str = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def delete_many(cursor: Cursor, delete_from: str, *, where: WhereType = None, returning: tuple[str, ...] | _TSTAR = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def delete_many(cursor: Cursor, delete_from: str, *, where: WhereType = None, returning: list[str] | _DSTAR = None, no_fetch: Literal[False] = False) -> list[dict[str, Any]]: ...


@overload
def delete_many(cursor: Cursor, delete_from: str, *, where: WhereType = None, returning: type[OutputModel] = None, no_fetch: Literal[False] = False) -> list[OutputModel]: ...


@overload
def delete_many(cursor: Cursor, delete_from: str, *, where: WhereType = None, returning: SelectType = None, no_fetch: Literal[True] = False) -> None: ...


def delete_many(
        cursor: Cursor,
        delete_from: str,
        *,
        where: WhereType = None,
        returning: SelectType = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = prepare_delete_query(delete_from, where, returning)
    cursor.execute(query)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
