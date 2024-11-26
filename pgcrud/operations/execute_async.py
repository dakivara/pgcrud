from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor
from psycopg.abc import Query

from pgcrud.col import Col
from pgcrud.operations.utils import get_async_row_factory, prepare_execute_params
from pgcrud.types import PydanticModel, ParamsValueItemType, ResultManyValueType, ReturningValueType


@overload
async def execute(
        cursor: AsyncCursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: Literal[None] = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
async def execute(
        cursor: AsyncCursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: Col,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
async def execute(
        cursor: AsyncCursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: Sequence[Col],
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
async def execute(
        cursor: AsyncCursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: type[PydanticModel],
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
async def execute(
        cursor: AsyncCursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: Literal[True],
) -> None: ...


async def execute(
        cursor: AsyncCursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    params = prepare_execute_params(params)
    await cursor.execute(query, params)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
