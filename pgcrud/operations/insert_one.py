from collections.abc import Sequence
from typing import Any, overload

from psycopg import Cursor

from pgcrud.col import Col
from pgcrud.operations.shared import get_row_factory, construct_composed_insert_query
from pgcrud.types import PydanticModel, InsertIntoValueType, AdditionalValuesType, ResultOneValueType, ReturningValueType, ValuesValueItemType


@overload
def insert_one(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
) -> None: ...


@overload
def insert_one(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: Col,
        additional_values: AdditionalValuesType | None = None,
) -> Any | None: ...


@overload
def insert_one(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: Sequence[Col],
        additional_values: AdditionalValuesType | None = None,
) -> tuple[Any, ...] | None: ...


@overload
def insert_one(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: type[PydanticModel],
        additional_values: AdditionalValuesType | None = None,
) -> PydanticModel | None: ...


def insert_one(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueItemType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
) -> ResultOneValueType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = construct_composed_insert_query(insert_into, (values,), returning, additional_values)
    cursor.execute(query)

    if returning:
        return cursor.fetchone()
