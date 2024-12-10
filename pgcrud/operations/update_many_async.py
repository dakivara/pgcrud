from typing import Literal, TypeVar, overload

from psycopg import AsyncCursor

from pgcrud.operations.shared import get_async_row_factory, construct_composed_update_query
from pgcrud.types import FromValueType, UpdateValueType, SetColsType, SetValuesType, WhereValueType, ReturningValueType, AdditionalValuesType


T = TypeVar('T')


@overload
async def update_many(
        cursor: AsyncCursor[T],
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def update_many(
        cursor: AsyncCursor[T],
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
async def update_many(
        cursor: AsyncCursor[T],
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor[T]: ...


async def update_many(
        cursor: AsyncCursor[T],
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[T] | AsyncCursor[T] | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = construct_composed_update_query(update, set_, from_,  where, returning, additional_values)
    await cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
