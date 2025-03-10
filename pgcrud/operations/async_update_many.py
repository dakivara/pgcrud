from typing import Literal, overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_update_query
from pgcrud.types import FromValueType, Row, UpdateValueType, SetValueType, WhereValueType, ReturningValueType, AdditionalValuesType


@overload
async def async_update_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def async_update_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
async def async_update_many(
        cursor: AsyncCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor[Row]: ...


@overload
async def async_update_many(
        cursor: AsyncServerCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncServerCursor[Row]: ...


async def async_update_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[Row] | AsyncCursor[Row] | AsyncServerCursor[Row] | None:

    query = construct_composed_update_query(update, set_, from_,  where, returning, additional_values)
    await cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
