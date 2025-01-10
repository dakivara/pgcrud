from collections.abc import Sequence
from typing import Literal, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, OnConflictValueType, ReturningValueType, Row, ValuesValueType


@overload
def insert_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def insert_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
def insert_many(
        cursor: Cursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> Cursor[Row]: ...


@overload
def insert_many(
        cursor: ServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> ServerCursor[Row]: ...


def insert_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        *,
        on_conflict: OnConflictValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[Row] | Cursor[Row] | ServerCursor[Row] | None:

    query = construct_composed_insert_query(insert_into, values, on_conflict, returning, additional_values)
    cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
