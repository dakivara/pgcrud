from typing import Any, overload

from psycopg import AsyncCursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
async def insert_one(cursor: AsyncCursor, insert_into: str, values: ValuesType, *, returning: str, exclude: ExcludeType = None, **kwargs) -> Any | None: ...


@overload
async def insert_one(cursor: AsyncCursor, insert_into: str, values: ValuesType, *, returning: tuple[str, ...] | _TSTAR, exclude: ExcludeType = None, **kwargs) -> tuple[Any, ...] | None: ...


@overload
async def insert_one(cursor: AsyncCursor, insert_into: str, values: ValuesType, *, returning: list[str] | _DSTAR, exclude: ExcludeType = None, **kwargs) -> dict[str, Any] | None: ...


@overload
async def insert_one(cursor: AsyncCursor, insert_into: str, values: ValuesType, *, returning: type[OutputModel], exclude: ExcludeType = None, **kwargs) -> OutputModel | None: ...


@overload
async def insert_one(cursor: AsyncCursor, insert_into: str, values: ValuesType, *, exclude: ExcludeType = None, **kwargs) -> None: ...


async def insert_one(cursor: AsyncCursor, insert_into: str, values: ValuesType, *, returning: SelectType = None, exclude: ExcludeType = None, **kwargs) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_insert_params(values, kwargs, exclude)
    query = prepare_insert_query(insert_into, params, returning)

    await cursor.execute(query, params)

    if returning:
        return await cursor.fetchone()
