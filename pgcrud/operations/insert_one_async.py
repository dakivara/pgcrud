from collections.abc import Sequence
from typing import Any, overload

from psycopg import AsyncCursor

from pgcrud.expr import Expr
from pgcrud.operations.shared import get_async_row_factory, construct_composed_insert_query
from pgcrud.types import PydanticModel, InsertIntoValueType, AdditionalValuesType, ResultOneValueType, ReturningValueType, ValuesValueItemType


@overload
async def insert_one(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
) -> None: ...


@overload
async def insert_one(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: Expr,
        additional_values: AdditionalValuesType | None = None,
) -> Any | None: ...


@overload
async def insert_one(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: Sequence[Expr],
        additional_values: AdditionalValuesType | None = None,
) -> tuple[Any, ...] | None: ...


@overload
async def insert_one(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: type[PydanticModel],
        additional_values: AdditionalValuesType | None = None,
) -> PydanticModel | None: ...


async def insert_one(
        cursor: AsyncCursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
) -> ResultOneValueType | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = construct_composed_insert_query(insert_into, (values,), returning, additional_values)
    await cursor.execute(query)

    if returning:
        return await cursor.fetchone()
