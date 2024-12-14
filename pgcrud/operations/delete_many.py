from typing import Literal, overload

from pgcrud.db import Cursor, ServerCursor
from pgcrud.operations.shared import construct_composed_delete_query
from pgcrud.types import DeleteFromValueType, ReturningValueType, Row, UsingValueType, WhereValueType


@overload
def delete_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def delete_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        no_fetch: Literal[False] = False,
) -> list[Row]: ...


@overload
def delete_many(
        cursor: Cursor[Row],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        no_fetch: Literal[True],
) -> Cursor[Row]: ...


@overload
def delete_many(
        cursor: ServerCursor[Row],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        no_fetch: Literal[True],
) -> ServerCursor[Row]: ...


def delete_many(
        cursor: Cursor[Row] | ServerCursor[Row],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> list[Row] | Cursor[Row] | ServerCursor[Row] | None:

    query = construct_composed_delete_query(delete_from, using, where, returning)
    cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
