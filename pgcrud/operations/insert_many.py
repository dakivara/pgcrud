from typing import Literal, TypeVar, overload

from psycopg import Cursor

from pgcrud.operations.shared import get_row_factory, construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, ReturningValueType, ValuesValueType


T = TypeVar('T')


@overload
def insert_many(
        cursor: Cursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def insert_many(
        cursor: Cursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
def insert_many(
        cursor: Cursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> Cursor[T]: ...


def insert_many(
        cursor: Cursor[T],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[T] | Cursor[T] | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = construct_composed_insert_query(insert_into, values, returning, additional_values)
    cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        if returning:
            return cursor.fetchall()
