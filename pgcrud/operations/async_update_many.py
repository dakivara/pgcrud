from collections.abc import Sequence
from typing import Any, Literal, overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.expressions.base import IdentifierExpression
from pgcrud.operations.shared import construct_composed_update_query
from pgcrud.types import Row


@overload
async def async_update_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
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
async def async_update_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
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
async def async_update_many(
        cursor: AsyncCursor[Row],
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        *,
        from_: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor[Row]: ...


@overload
async def async_update_many(
        cursor: AsyncServerCursor[Row],
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        *,
        from_: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any],
        additional_values: dict[str, Any] | None = None,
        no_fetch: Literal[True],
) -> AsyncServerCursor[Row]: ...


async def async_update_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        *,
        from_: Any | None = None,
        where: Any | None = None,
        returning: Any | Sequence[Any] | None = None,
        additional_values: dict[str, Any] | None = None,
        no_fetch: bool = False,
) -> list[Row] | AsyncCursor[Row] | AsyncServerCursor[Row] | None:

    query = construct_composed_update_query(update, set_, from_,  where, returning, additional_values)
    await cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
