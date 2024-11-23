from collections.abc import Sequence
from typing import Any, overload

from psycopg import Cursor

from pgcrud.col import Col
from pgcrud.operations.type_hints import *
from pgcrud.operations.utils import *


@overload
def insert_one(cursor: Cursor, insert_into: TableType, values: ValuesType, *, additional_values: AdditionalValuesType | None = None, returning: None = None, exclude: ExcludeType | None = None) -> None: ...


@overload
def insert_one(cursor: Cursor, insert_into: TableType, values: ValuesType, *, additional_values: AdditionalValuesType | None = None, returning: str | Col, exclude: ExcludeType | None = None) -> Any | None: ...


@overload
def insert_one(cursor: Cursor, insert_into: TableType, values: ValuesType, *, additional_values: AdditionalValuesType | None = None, returning: Sequence[str | Col], exclude: ExcludeType | None = None) -> tuple[Any, ...] | None: ...


@overload
def insert_one(cursor: Cursor, insert_into: TableType, values: ValuesType, *, additional_values: AdditionalValuesType | None = None, returning: type[PydanticModel], exclude: ExcludeType | None = None) -> PydanticModel | None: ...


def insert_one(
        cursor: Cursor,
        insert_into: TableType,
        values: ValuesType,
        *,
        additional_values: AdditionalValuesType | None = None,
        returning: SelectType | None = None,
        exclude: ExcludeType | None = None,
) -> ReturnType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_insert_params(values, additional_values, exclude)
    query = prepare_insert_query(insert_into, [params], returning)

    cursor.execute(query)

    if returning:
        return cursor.fetchone()
