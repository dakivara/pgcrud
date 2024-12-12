from typing import Any, Literal, TypeVar, overload

from psycopg import Cursor

from pgcrud.operations.shared import get_row_factory, construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, ReturningValueType, ValuesValueType


T = TypeVar('T')


@overload
def insert_many(
        cursor: Cursor[Any],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: None = None,
        as_: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def insert_many(
        cursor: Cursor[Any],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        as_: type[T],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
def insert_many(
        cursor: Cursor[Any],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType,
        as_: type[T],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> Cursor[T]: ...


def insert_many(
        cursor: Cursor[Any],
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        as_: type[T] | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[T] | Cursor[T] | None:

    if returning and as_:
        cursor.row_factory = get_row_factory(as_)

    query = construct_composed_insert_query(insert_into, values, returning, additional_values)
    cursor.execute(query)

    if returning and as_:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
