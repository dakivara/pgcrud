from typing import Any, Literal, TypeVar, overload

from psycopg import AsyncCursor

from pgcrud.operations.shared import get_async_row_factory, construct_composed_update_query
from pgcrud.types import FromValueType, UpdateValueType, SetColsType, SetValuesType, WhereValueType, ReturningValueType, AdditionalValuesType


T = TypeVar('T')


@overload
async def update_many(
        cursor: AsyncCursor[Any],
        update: UpdateValueType,
        set_columns: SetColsType,
        set_values: SetValuesType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        as_: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def update_many(
        cursor: AsyncCursor[Any],
        update: UpdateValueType,
        set_columns: SetColsType,
        set_values: SetValuesType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        as_: type[T],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
async def update_many(
        cursor: AsyncCursor[Any],
        update: UpdateValueType,
        set_columns: SetColsType,
        set_values: SetValuesType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        as_: type[T],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> AsyncCursor[T]: ...


async def update_many(
        cursor: AsyncCursor[Any],
        update: UpdateValueType,
        set_columns: SetColsType,
        set_values: SetValuesType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        as_: type[T] | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[T] | AsyncCursor[T] | None:

    if returning and as_:
        cursor.row_factory = get_async_row_factory(as_)

    query = construct_composed_update_query(update, set_columns, set_values, from_,  where, returning, additional_values)
    await cursor.execute(query)

    if returning and as_:
        if no_fetch:
            return cursor
        else:
            return await cursor.fetchall()
