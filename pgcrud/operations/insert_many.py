from collections.abc import Sequence
from typing import Any, Literal, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.expressions.base import IdentifierExpression
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import Row


@overload
def insert_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Sequence[Any],
        *,
        # on_conflict: Any | None = None,
        returning: None = None,
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def insert_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Sequence[Any],
        *,
        # on_conflict: Any | None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
def insert_many(
        cursor: Cursor[Row],
        insert_into: IdentifierExpression,
        values: Sequence[Any],
        *,
        # on_conflict: Any | None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[True],
) -> Cursor[Row]: ...


@overload
def insert_many(
        cursor: ServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Sequence[Any],
        *,
        # on_conflict: Any | None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[True],
) -> ServerCursor[Row]: ...


def insert_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Sequence[Any],
        *,
        # on_conflict: Any | None = None,
        returning: Any | Sequence[Any] | None = None,
        additional_values: dict[str, Any] | None = None,
        no_fetch: bool = False,
) -> list[Row] | Cursor[Row] | ServerCursor[Row] | None:

    query = construct_composed_insert_query(insert_into, values, returning, additional_values)
    cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
