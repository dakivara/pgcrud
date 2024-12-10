from typing import Literal, TypeVar, overload

from psycopg import Cursor

from pgcrud.operations.shared import get_row_factory, construct_composed_delete_query
from pgcrud.types import DeleteFromValueType, ReturningValueType, UsingValueType, WhereValueType


T = TypeVar('T')


@overload
def delete_many(
        cursor: Cursor[T],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def delete_many(
        cursor: Cursor[T],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
def delete_many(
        cursor: Cursor[T],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        no_fetch: Literal[True],
) -> Cursor[T]: ...


def delete_many(
        cursor: Cursor[T],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> list[T] | Cursor[T] | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = construct_composed_delete_query(delete_from, using, where, returning)
    cursor.execute(query)

    if returning:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
