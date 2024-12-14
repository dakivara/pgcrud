from typing import overload


from pgcrud.db import Cursor, ServerCursor
from pgcrud.operations.shared import construct_composed_insert_query
from pgcrud.types import InsertIntoValueType, AdditionalValuesType, ReturningValueType, Row, ValuesValueItemType


@overload
def insert_one(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
) -> None: ...


@overload
def insert_one(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
) -> Row | None: ...


def insert_one(
        cursor: Cursor[Row] | ServerCursor[Row],
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
) -> Row | None:

    query = construct_composed_insert_query(insert_into, (values,), returning, additional_values)
    cursor.execute(query)

    if returning:
        return cursor.fetchone()
