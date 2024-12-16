from typing import Literal, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.operations.shared import construct_composed_update_query
from pgcrud.types import FromValueType, Row, UpdateValueType, SetValueType, WhereValueType, ReturningValueType, AdditionalValuesType


@overload
def update_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def update_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
def update_many(
        cursor: Cursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> Cursor[Row]: ...


@overload
def update_many(
        cursor: ServerCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: Literal[True],
) -> ServerCursor[Row]: ...


def update_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        update: UpdateValueType,
        set_: SetValueType,
        *,
        from_: FromValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        additional_values: AdditionalValuesType | None = None,
        no_fetch: bool = False,
) -> list[Row] | Cursor[Row] | ServerCursor[Row] | None:

    query = construct_composed_update_query(update, set_[0], set_[1], from_, where, returning, additional_values)
    cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
