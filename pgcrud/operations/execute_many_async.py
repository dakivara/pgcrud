from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor
from psycopg.abc import Query

from pgcrud.col import Col
from pgcrud.operations.type_hints import *
from pgcrud.operations.utils import *


@overload
async def execute_many(cursor: AsyncCursor, query: Query, params: Sequence[ParamsType], *, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
async def execute_many(cursor: AsyncCursor, query: Query, params: Sequence[ParamsType], *, returning: str | Col, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
async def execute_many(cursor: AsyncCursor, query: Query, params: Sequence[ParamsType], *, returning: Sequence[str | Col], no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
async def execute_many(cursor: AsyncCursor, query: Query, params: Sequence[ParamsType], *, returning: type[PydanticModel], no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
async def execute_many(cursor: AsyncCursor, query: Query,params: Sequence[ParamsType], *, returning: SelectType | None = None, no_fetch: Literal[True]) -> None: ...


async def execute_many(
        cursor: AsyncCursor,
        query: Query,
        params: Sequence[ParamsType],
        *,
        returning: SelectType | None = None,
        no_fetch: bool = False,
) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    params = prepare_execute_params_seq(params)
    await cursor.executemany(query, params, returning=True if returning else False)

    if not no_fetch:
        if returning:
            rows = []

            while True:
                rows.append(await cursor.fetchone())
                if not cursor.nextset():
                    break

            return rows
