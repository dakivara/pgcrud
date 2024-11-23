from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud.col import Col
from pgcrud.operations.type_hints import *
from pgcrud.operations.utils import *


@overload
def insert_many(cursor: Cursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: Literal[None] = None, exclude: ExcludeType | None, no_fetch: Literal[False]) -> None: ...


@overload
def insert_many(cursor: Cursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: str | Col, exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def insert_many(cursor: Cursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: Sequence[str | Col], exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def insert_many(cursor: Cursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: type[PydanticModel], exclude: ExcludeType | None = None, no_fetch: Literal[False] = False) -> list[PydanticModel]: ...


@overload
def insert_many(cursor: Cursor, insert_into: TableType, values: Sequence[ValuesType], *, additional_values: AdditionalValuesType | None = None, returning: SelectType | None = None, exclude: ExcludeType | None = None, no_fetch: Literal[True]) -> None: ...


def insert_many(
        cursor: Cursor,
        insert_into: TableType,
        values: Sequence[ValuesType],
        *,
        additional_values: AdditionalValuesType | None = None,
        returning: SelectType | None = None,
        exclude: ExcludeType | None = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:

    if len(values) == 0:
        raise ValueError('Input list must have at least one element')

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = [prepare_insert_params(val, additional_values, exclude) for val in values]
    query = prepare_insert_query(insert_into, params, returning)

    cursor.execute(query)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
