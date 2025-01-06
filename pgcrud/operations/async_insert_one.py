from typing import overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, ReturningValueType, Row, ValuesValueType


@overload
async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
) -> None: ...


@overload
async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
) -> Row | None: ...


async def async_insert_one(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
) -> Row | None:

    query = construct_composed_insert_query(insert_into, [values], returning, additional_values)
    await cursor.execute(query)

    if returning:
        return await cursor.fetchone()
