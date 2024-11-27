from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud.col import Col
from pgcrud.operations.shared import get_row_factory, construct_composed_delete_query
from pgcrud.types import PydanticModel, DeleteFromValueType, ResultManyValueType, ReturningValueType, UsingValueType, WhereValueType


@overload
def delete_many(
        cursor: Cursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: None = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def delete_many(
        cursor: Cursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: Col,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
def delete_many(
        cursor: Cursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: Sequence[Col],
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
def delete_many(
        cursor: Cursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: type[PydanticModel],
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
def delete_many(
        cursor: Cursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: Literal[True],
) -> None: ...


def delete_many(
        cursor: Cursor,
        delete_from: DeleteFromValueType,
        *,
        using: UsingValueType | None = None,
        where: WhereValueType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    query = construct_composed_delete_query(delete_from, using, where, returning)
    cursor.execute(query)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
