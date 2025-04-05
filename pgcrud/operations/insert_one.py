from collections.abc import Sequence
from typing import Any, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.expressions.base import IdentifierExpression
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import Row


@overload
def insert_one(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Any,
        *,
        # on_conflict: Any | None = None,
        returning: None = None,
        additional_values: dict[str, Any] | None = None,
) -> None: ...


@overload
def insert_one(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Any,
        *,
        # on_conflict_on_constraint: None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
) -> Row: ...


# @overload
# def insert_one(
#         cursor: Cursor[Row] | ServerCursor[Row],
#         insert_into: IdentifierExpression,
#         values: Any,
#         *,
#         # on_conflict: Any,
#         returning: Any | Sequence[Any],
#         additional_values: dict[str, Any] | None = None,
# ) -> Row | None: ...


def insert_one(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Any,
        *,
        # on_conflict: Any | None = None,
        returning: Any | Sequence[Any] | None = None,
        additional_values: dict[str, Any] | None = None,
) -> Row | None:

    query = construct_composed_insert_query(insert_into, [values], returning, additional_values)
    cursor.execute(query)

    if returning:
        return cursor.fetchone()
