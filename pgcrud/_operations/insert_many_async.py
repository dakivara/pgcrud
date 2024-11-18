from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import AsyncCursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
async def insert_many(cursor: AsyncCursor, into: str, values: Sequence[ValuesType], *, returning: Literal[None] = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> None: ...


@overload
async def insert_many(cursor: AsyncCursor, into: str, values: Sequence[ValuesType], *, returning: str = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[Any]: ...


@overload
async def insert_many(cursor: AsyncCursor, into: str, values: Sequence[ValuesType], *, returning: tuple[str, ...] | _TSTAR = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[tuple[Any, ...]]: ...


@overload
async def insert_many(cursor: AsyncCursor, into: str, values: Sequence[ValuesType], *, returning: list[str] | _DSTAR = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[dict[str, Any]]: ...


@overload
async def insert_many(cursor: AsyncCursor, into: str, values: Sequence[ValuesType], *, returning: type[OutputModel] = None, exclude: ExcludeType = None, no_fetch: Literal[False] = False, **kwargs) -> list[OutputModel]: ...


@overload
async def insert_many(cursor: AsyncCursor, into: str, values: Sequence[ValuesType], *, returning: SelectType = None, exclude: ExcludeType = None, no_fetch: Literal[True] = False, **kwargs) -> None: ...


async def insert_many(
        cursor: AsyncCursor,
        into: str,
        values: Sequence[ValuesType],
        *,
        returning: SelectType = None,
        exclude: ExcludeType = None,
        no_fetch: bool = False,
        **kwargs,
) -> list[ReturnType] | None:

    if len(values) == 0:
        raise ValueError('Input list must have at least one element')

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = [prepare_insert_params(val, kwargs, exclude) for val in values]
    query = prepare_insert_query(into, params[0], returning)

    await cursor.executemany(query, params, returning=True if returning else False)

    if not no_fetch:
        if returning:
            rows = []

            while True:
                rows.append(await cursor.fetchone())
                if not cursor.nextset():
                    break

            return rows
