from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud.col import Col
from pgcrud.operations.type_hints import *
from pgcrud.operations.utils import *


@overload
async def insert_one(cursor: AsyncCursor, insert_into: TableType, values: ValuesType, *, additional_values: AdditionalValuesType | None = None, returning: Literal[None] = None, exclude: ExcludeType | None = None) -> None: ...


@overload
async def insert_one(cursor: AsyncCursor, insert_into: TableType, values: ValuesType, *, additional_values: AdditionalValuesType | None = None, returning: str | Col, exclude: ExcludeType | None = None) -> Any | None: ...


@overload
async def insert_one(cursor: AsyncCursor, insert_into: TableType, values: ValuesType, *, additional_values: AdditionalValuesType | None = None, returning: Sequence[str | Col], exclude: ExcludeType | None = None) -> tuple[Any, ...] | None: ...


@overload
async def insert_one(cursor: AsyncCursor, insert_into: TableType, values: ValuesType, *, additional_values: AdditionalValuesType | None = None, returning: type[PydanticModel], exclude: ExcludeType | None = None) -> PydanticModel | None: ...


async def insert_one(
        cursor: AsyncCursor,
        insert_into: TableType,
        values: ValuesType,
        *,
        additional_values: AdditionalValuesType | None = None,
        returning: SelectType | None = None,
        exclude: ExcludeType | None = None,
) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    params = prepare_insert_params(values, additional_values, exclude)
    query = prepare_insert_query(insert_into, [params], returning)

    await cursor.execute(query, params)

    if returning:
        return await cursor.fetchone()
