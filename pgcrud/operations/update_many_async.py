from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud.col import Col
from pgcrud.operations.utils import get_async_row_factory, construct_composed_update_query
from pgcrud.types import FromValueType, PydanticModel, UpdateValueType, SetColsType, SetValueType, WhereValueType, ReturningValueType, AdditionalValuesType, ResultManyValueType


@overload
async def update_many(
        cursor: AsyncCursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValueType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def update_many(
        cursor: AsyncCursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValueType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: Col,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
async def update_many(
        cursor: AsyncCursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValueType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: Sequence[Col],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
async def update_many(
        cursor: AsyncCursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValueType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: type[PydanticModel],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
async def update_many(
        cursor: AsyncCursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValueType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> None: ...


async def update_many(
        cursor: AsyncCursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValueType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    query = construct_composed_update_query(update, set_, from_,  where, returning, additional_values)
    await cursor.execute(query)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
