from typing import Any, overload

from psycopg import Cursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
def insert_one(cursor: Cursor, insert_into: str, values: ValuesType, *, returning: str, exclude: ExcludeType = None, **kwargs) -> Any | None: ...


@overload
def insert_one(cursor: Cursor, insert_into: str, values: ValuesType, *, returning: tuple[str, ...] | _TSTAR, exclude: ExcludeType = None, **kwargs) -> tuple[Any, ...] | None: ...


@overload
def insert_one(cursor: Cursor, insert_into: str, values: ValuesType, *, returning: list[str] | _DSTAR, exclude: ExcludeType = None, **kwargs) -> dict[str, Any] | None: ...


@overload
def insert_one(cursor: Cursor, insert_into: str, values: ValuesType, *, returning: type[OutputModel], exclude: ExcludeType = None, **kwargs) -> OutputModel | None: ...


@overload
def insert_one(cursor: Cursor, insert_into: str, values: ValuesType, *, exclude: ExcludeType = None, **kwargs) -> None: ...


def insert_one(
        cursor: Cursor,
        insert_into: str,
        values: ValuesType,
        *,
        returning: SelectType = None,
        exclude: ExcludeType = None,
        **kwargs,
) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_insert_params(values, kwargs, exclude)
    query = prepare_insert_query(insert_into, params, returning)

    cursor.execute(query, params)

    if returning:
        return cursor.fetchone()
