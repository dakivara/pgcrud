from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
def update_many(cursor: Cursor, update: str, set_: SetType, *, where: WhereType = None, returning: Literal[None] = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> None: ...


@overload
def update_many(cursor: Cursor, update: str, set_: SetType, *, where: WhereType = None, returning: str = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[Any]: ...


@overload
def update_many(cursor: Cursor, update: str, set_: SetType, *, where: WhereType = None, returning: tuple[str, ...] | _TSTAR = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[tuple[Any, ...]]: ...


@overload
def update_many(cursor: Cursor, update: str, set_: SetType, *, where: WhereType = None, returning: list[str] | _DSTAR = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[dict[str, Any]]: ...


@overload
def update_many(cursor: Cursor, update: str, set_: SetType, *, where: WhereType = None, returning: type[OutputModel] = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[OutputModel]: ...


@overload
def update_many(cursor: Cursor, update: str, set_: SetType, *, where: WhereType = None, returning: SelectType = None, exclude: ExcludeType = None, no_fetch: Literal[True] = False, **kwargs) -> None: ...


def update_many(
        cursor: Cursor,
        update: str,
        set_: SetType,
        *,
        where: WhereType = None,
        returning: SelectType = None,
        exclude: ExcludeType = None,
        no_fetch: bool = False,
        **kwargs,
) -> list[ReturnType] | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = prepare_update_query(update, set_, where, returning, exclude, kwargs)
    cursor.execute(query)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
