from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor
from psycopg.abc import Query

from pgcrud.col import Col
from pgcrud.operations.utils import get_async_row_factory, prepare_execute_many_params
from pgcrud.types import PydanticModel, ParamsValueType, ResultManyValueType, ReturningValueType


@overload
async def execute_many(
        cursor: AsyncCursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: Literal[None] = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def execute_many(
        cursor: AsyncCursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: Col,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
async def execute_many(
        cursor: AsyncCursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: Sequence[Col],
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
async def execute_many(
        cursor: AsyncCursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: type[PydanticModel],
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
async def execute_many(
        cursor: AsyncCursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: ReturningValueType | None = None,
        no_fetch: Literal[True],
) -> None: ...


async def execute_many(
        cursor: AsyncCursor,
        query: Query,
        params: ParamsValueType,
        *,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    params = prepare_execute_many_params(params)
    await cursor.executemany(query, params, returning=True if returning else False)

    if not no_fetch:
        if returning:
            rows = []

            while True:
                rows += await cursor.fetchall()
                if not cursor.nextset():
                    break

            return rows
