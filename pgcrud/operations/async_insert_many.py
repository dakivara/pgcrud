from collections.abc import Sequence
from typing import Literal, overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, OnConflictValueType, ReturningValueType, Row, ValuesValueType


@overload
async def async_insert_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def async_insert_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
async def async_insert_many(
        cursor: AsyncCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor[Row]: ...


@overload
async def async_insert_many(
        cursor: AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncServerCursor[Row]: ...


async def async_insert_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[Row] | AsyncCursor[Row] | AsyncServerCursor[Row] | None:

    query = construct_composed_insert_query(insert_into, values, on_conflict, returning, additional_values)
    await cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
