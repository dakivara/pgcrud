from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud.expr import Expr
from pgcrud.operations.shared import get_async_row_factory, construct_composed_insert_query
from pgcrud.types import PydanticModel, InsertIntoValueType, AdditionalValuesType, ResultManyValueType, ReturningValueType, ValuesValueType


@overload
async def insert_many(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def insert_many(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: Expr,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
async def insert_many(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: Sequence[Expr],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
async def insert_many(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: type[PydanticModel],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
async def insert_many(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor: ...


async def insert_many(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | AsyncCursor | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = construct_composed_insert_query(insert_into, values, returning, additional_values)
    await cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        if returning:
            return await cursor.fetchall()
