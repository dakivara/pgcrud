from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud.expr import Expr
from pgcrud.operations.shared import get_row_factory, construct_composed_update_query
from pgcrud.types import FromValueType, PydanticModel, UpdateValueType, SetColsType, SetValuesType, WhereValueType, ReturningValueType, AdditionalValuesType, ResultManyValueType


@overload
def update_many(
        cursor: Cursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def update_many(
        cursor: Cursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: Expr,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
def update_many(
        cursor: Cursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: Sequence[Expr],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
def update_many(
        cursor: Cursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: type[PydanticModel],
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
def update_many(
        cursor: Cursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> Cursor: ...


def update_many(
        cursor: Cursor,
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValuesType],
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | Cursor | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = construct_composed_update_query(update, set_, from_, where, returning, additional_values)
    cursor.execute(query)

    if no_fetch:
        return cursor
    else:
        if returning:
            return cursor.fetchall()
