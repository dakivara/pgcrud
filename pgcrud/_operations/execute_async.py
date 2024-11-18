from typing import Any, Literal, overload

from psycopg import AsyncCursor
from psycopg.abc import Query

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType = None, returning: Literal[None] = None, no_fetch: Literal[False] = False) -> None: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType = None, returning: str = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType = None, returning: tuple[str, ...] | _TSTAR = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType = None, returning: list[str] | _DSTAR = None, no_fetch: Literal[False] = False) -> list[dict[str, Any]]: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType = None, returning: type[OutputModel] = None, no_fetch: Literal[False] = False) -> list[OutputModel]: ...


@overload
async def execute(cursor: AsyncCursor, query: Query, *, params: ParamsType = None, returning: SelectType = None, no_fetch: Literal[True] = False) -> None: ...


async def execute(
        cursor: AsyncCursor,
        query: Query,
        *,
        params: ParamsType = None,
        returning: SelectType = None,
        no_fetch: bool = False,
) -> ReturnType | None:
    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_execute_params(params)
    await cursor.execute(query, params)

    if not no_fetch:
        if returning:
            return await cursor.fetchall()
