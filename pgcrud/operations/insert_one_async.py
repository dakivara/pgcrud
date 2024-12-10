from typing import TypeVar, overload

from psycopg import AsyncCursor

from pgcrud.operations.shared import get_async_row_factory, construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, ReturningValueType, ValuesValueItemType


T = TypeVar('T')


@overload
async def insert_one(
        cursor: AsyncCursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
) -> None: ...


@overload
async def insert_one(
        cursor: AsyncCursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
) -> T | None: ...


async def insert_one(
        cursor: AsyncCursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
) -> T | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = construct_composed_insert_query(insert_into, (values,), returning, additional_values)
    await cursor.execute(query)

    if returning:
        return await cursor.fetchone()
