from typing import Literal, TypeVar, overload

from psycopg import AsyncCursor

from pgcrud.operations.shared import get_async_row_factory, construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, ReturningValueType, ValuesValueType


T = TypeVar('T')


@overload
async def insert_many(
        cursor: AsyncCursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def insert_many(
        cursor: AsyncCursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
async def insert_many(
        cursor: AsyncCursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor[T]: ...


async def insert_many(
        cursor: AsyncCursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[T] | AsyncCursor[T] | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = construct_composed_insert_query(insert_into, values, returning, additional_values)
    await cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
