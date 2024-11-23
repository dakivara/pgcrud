from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor
from psycopg.abc import Query

from pgcrud._col import Col
from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType | None = None, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType | None = None, returning: str | Col, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType | None = None, returning: Sequence[str | Col], no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType | None = None, returning: type[PydanticModel], no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType | None = None, returning: SelectType | None = None, no_fetch: Literal[True]) -> None: ...


async def execute(
        cursor: AsyncCursor,
        query: Query,
        *,
        params: ParamsType | None = None,
        returning: SelectType | None = None,
        no_fetch: bool = False,
) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_async_row_factory(returning)

    params = prepare_execute_params(params)
    await cursor.execute(query, params)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
