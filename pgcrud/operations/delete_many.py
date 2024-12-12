from typing import Any, Literal, TypeVar, overload

from psycopg import Cursor

from pgcrud.operations.shared import get_row_factory, construct_composed_delete_query
from pgcrud.types import DeleteFromValueType, ReturningValueType, UsingValueType, WhereValueType


T = TypeVar('T')


@overload
def delete_many(
        cursor: Cursor[Any],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        as_: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def delete_many(
        cursor: Cursor[Any],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        as_: type[T],
        no_fetch: Literal[False] = False,
) -> list[T]: ...


@overload
def delete_many(
        cursor: Cursor[Any],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType,
        as_: type[T],
        no_fetch: Literal[True],
) -> Cursor[T]: ...


def delete_many(
        cursor: Cursor[Any],
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        as_: type[T] | None = None,
        no_fetch: bool = False,
) -> list[T] | Cursor[T] | None:

    if returning and as_:
        cursor.row_factory = get_row_factory(as_)

    query = construct_composed_delete_query(delete_from, using, where, returning)
    cursor.execute(query)

    if returning and as_:
        if no_fetch:
            return cursor
        else:
            return cursor.fetchall()
