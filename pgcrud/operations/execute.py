from collections.abc import Sequence
from typing import Any, Literal, overload

from psycopg import Cursor
from psycopg.abc import Query

from pgcrud.col import Col
from pgcrud.operations.utils import get_row_factory, prepare_execute_params
from pgcrud.types import PydanticModel, ParamsValueItemType, ResultManyValueType, ReturningValueType


@overload
def execute(
        cursor: Cursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: Literal[None] = None,
        no_fetch: Literal[False] = False,
) -> None: ...


@overload
def execute(
        cursor: Cursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: Col,
        no_fetch: Literal[False] = False,
) -> list[Any]: ...


@overload
def execute(
        cursor: Cursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: Sequence[Col],
        no_fetch: Literal[False] = False,
) -> list[tuple[Any, ...]]: ...


@overload
def execute(
        cursor: Cursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: type[PydanticModel],
        no_fetch: Literal[False] = False,
) -> list[PydanticModel]: ...


@overload
def execute(
        cursor: Cursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: Literal[True],
) -> None: ...


def execute(
        cursor: Cursor,
        query: Query,
        *,
        params: ParamsValueItemType | None = None,
        returning: ReturningValueType | None = None,
        no_fetch: bool = False,
) -> ResultManyValueType | None:

    if returning:
        cursor.row_factory = get_row_factory(returning)

    params = prepare_execute_params(params)
    cursor.execute(query, params)

    if not no_fetch:
        if returning:
            return cursor.fetchall()
