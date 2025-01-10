from typing import overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, OnConflictValueType, ReturningValueType, Row, ValuesValueType


@overload
async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
) -> None: ...


@overload
async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        on_conflict: None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
) -> Row: ...


@overload
async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        on_conflict: OnConflictValueType,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
) -> Row | None: ...


async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
) -> Row | None:

    query = construct_composed_insert_query(insert_into, [values], on_conflict, returning, additional_values)
    await cursor.execute(query)

    if returning:
        return await cursor.fetchone()
