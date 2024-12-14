from typing import Literal, overload

from pgcrud.db import AsyncCursor, AsyncServerCursor
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, ReturningValueType, Row, ValuesValueType


@overload
async def insert_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def insert_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
async def insert_many(
        cursor: AsyncCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor[Row]: ...


@overload
async def insert_many(
        cursor: AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncServerCursor[Row]: ...


async def insert_many(
        cursor: AsyncCursor[Row] | AsyncServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[Row] | AsyncCursor[Row] | AsyncServerCursor[Row] | None:

    query = construct_composed_insert_query(insert_into, values, returning, additional_values)
    await cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
