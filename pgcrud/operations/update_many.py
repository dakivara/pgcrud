from collections.abc import Sequence
from typing import Any, Literal, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.expressions.base import IdentifierExpression
from pgcrud.operations.shared import construct_composed_update_query
from pgcrud.types import Row


@overload
def update_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        *,
        from_: Any | None = None,
        where: Any | None = None,
        returning: None = None,
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def update_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        *,
        from_: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
def update_many(
        cursor: Cursor[Row],
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        *,
        from_: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[True],
) -> Cursor[Row]: ...


@overload
def update_many(
        cursor: ServerCursor[Row],
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        *,
        from_: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[True],
) -> ServerCursor[Row]: ...


def update_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        *,
        from_: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any] | None = None,
        additional_values: dict[str, Any] | None = None,
        no_fetch: bool = False,
) -> list[Row] | Cursor[Row] | ServerCursor[Row] | None:

    query = construct_composed_update_query(update, set_, from_, where, returning, additional_values)
    cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
