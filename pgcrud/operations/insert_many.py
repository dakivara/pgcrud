from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud.expr import Expr
from pgcrud.operations.shared import get_row_factory, construct_composed_insert_query
from pgcrud.types import PydanticModel, InsertIntoValueType, AdditionalValuesType, ResultManyValueType, ReturningValueType, ValuesValueType


@overload
def insert_many(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def insert_many(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: Expr,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
def insert_many(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: Sequence[Expr],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
def insert_many(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: type[PydanticModel],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
def insert_many(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> None: ...


def insert_many(
        cursor: Cursor,
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        *,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = construct_composed_insert_query(insert_into, values, returning, additional_values)
    cursor.execute(query)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
