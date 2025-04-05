from collections.abc import Sequence
from typing import Any, overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.expressions.base import IdentifierExpression
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import Row


@overload
async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Any,
        *,
        # on_conflict: Any | None = None,
        returning: None = None,
        additional_values: dict[str, Any] | None = None,
) -> None: ...


@overload
async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Any,
        *,
        # on_conflict: None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
) -> Row: ...


# @overload
# async def async_insert_one(
#         cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
#         insert_into: IdentifierExpression,
#         values: Any,
#         *,
#         # on_conflict: Any,
#         returning: Any | Sequence[Any],
#         additional_values: dict[str, Any] | None = None,
# ) -> Row | None: ...


async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: IdentifierExpression,
        values: Any,
        *,
        # on_conflict: Any | None = None,
        returning: Any | Sequence[Any] | None = None,
        additional_values: dict[str, Any] | None = None,
) -> Row | None:

    query = construct_composed_insert_query(insert_into, [values], returning, additional_values)
    await cursor.execute(query)

    if returning:
        return await cursor.fetchone()
