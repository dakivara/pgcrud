from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
async def insert_many(cursor: AsyncCursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: Literal[None] = None, exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> None: ...


@overload
async def insert_many(cursor: AsyncCursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: str | Col, exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
async def insert_many(cursor: AsyncCursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: Sequence[str | Col], exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
async def insert_many(cursor: AsyncCursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: type[PydanticModel], exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
async def insert_many(cursor: AsyncCursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: SelectType | None = None, exclude: ExcludeType | None = None, no_fetch: Literal[True]) -> None: ...


async def insert_many(
        cursor: AsyncCursor,
        insert_into: TableType,
        values: Sequence[ValuesType],
        *,
        additional_values: AdditionalValuesType | None = None,
        returning: SelectType | None = None,
        exclude: ExcludeType | None = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:

    if len(values) == 0:
        raise ValueError('Input list must have at least one element')

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    params = [prepare_insert_params(val, additional_values, exclude) for val in values]
    query = prepare_insert_query(insert_into, params, returning)

    await cursor.execute(query)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
