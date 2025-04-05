from collections.abc import Sequence
from typing import Any, Literal, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.operations.shared import construct_composed_delete_query
from pgcrud.types import Row


@overload
def delete_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def delete_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
def delete_many(
        cursor: Cursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        no_fetch: Literal[True],
) -> Cursor[Row]: ...


@overload
def delete_many(
        cursor: ServerCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        no_fetch: Literal[True],
) -> ServerCursor[Row]: ...


def delete_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        delete_from: Any,
        *,
        using: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any] | None = None,
        no_fetch: bool = False,
) -> list[Row] | Cursor[Row] | ServerCursor[Row] | None:

    query = construct_composed_delete_query(delete_from, using, where, returning)
    cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
