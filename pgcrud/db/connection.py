# pyright: reportIncompatibleMethodOverride=false, reportIncompatibleVariableOverride=false

from typing import Any, Literal, cast, overload

import psycopg
from psycopg.abc import AdaptContext, ConnParam
from psycopg.pq.abc import PGconn
from psycopg.rows import RowFactory, AsyncRowFactory, tuple_row

from pgcrud.config import config, ConfigDict
from pgcrud.db.cursor import Cursor, ServerCursor, AsyncCursor, AsyncServerCursor
from pgcrud.db.shared import get_row_factory, get_params
from pgcrud.query import Query
from pgcrud.types import ParamsType, QueryType, Row, T, ValidationType


__all__ = [
    'Connection',
    'AsyncConnection',
]


class Connection(psycopg.Connection[Row]):

    cursor_factory: type[Cursor[Row]]
    server_cursor_factory: type[ServerCursor[Row]]

    def __init__(
        self,
        pgconn: PGconn,
    ):
        super().__init__(pgconn, cast(RowFactory[Row], tuple_row))
        self.cursor_factory = Cursor
        self.server_cursor_factory = ServerCursor

    def __getitem__(self, item: type[T] | tuple[type[T], ConfigDict]) -> 'Connection[T]':
        row_type, validate, strict = get_params(item)
        self.row_factory = get_row_factory(row_type, validate, strict)  # type: ignore
        return self  # type: ignore

    @classmethod
    def connect(
        cls,
        conninfo: str = "",
        *,
        autocommit: bool = False,
        prepare_threshold: int | None = 5,
        context: AdaptContext | None = None,
        row_type: type[T] = tuple[Any, ...],
        validate: ValidationType = config.validation,
        strict: bool = config.strict,
        **kwargs: ConnParam,
    ) -> 'Connection[T]':

        return super().connect(
            conninfo=conninfo,
            autocommit=autocommit,
            prepare_threshold=prepare_threshold,
            context=context,
            row_factory=cast(RowFactory[Row], get_row_factory(row_type, validate, strict)),
            cursor_factory=Cursor,
            **kwargs,  # type: ignore
        )

    @overload
    def cursor(  # noqa
            self,
            name: Literal[""] = "",
    ) -> Cursor[Row]: ...

    @overload
    def cursor(  # noqa
            self,
            name: str,
    ) -> ServerCursor[Row]: ...

    def cursor(  # noqa
        self,
        name: str = "",
    ) -> Cursor[Row] | ServerCursor[Row]:

        return super().cursor(
            name=name,
        )  # type: ignore

    def execute(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        prepare: bool | None = None,
        binary: bool = False,
    ) -> Cursor[Row]:

        return super().execute(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=params,
            prepare=prepare,
            binary=binary,
        )  # type: ignore


class AsyncConnection(psycopg.AsyncConnection[Row]):

    cursor_factory: type[AsyncCursor[Row]]
    server_cursor_factory: type[AsyncServerCursor[Row]]

    def __init__(
        self,
        pgconn: PGconn,
    ):
        super().__init__(pgconn, cast(AsyncRowFactory[Row], tuple_row))
        self.cursor_factory = AsyncCursor
        self.server_cursor_factory = AsyncServerCursor

    def __getitem__(self, item: type[T] | tuple[type[T], ConfigDict]) -> 'AsyncConnection[T]':
        row_type, validate, strict = get_params(item)
        self.row_factory = get_row_factory(row_type, validate, strict)  # type: ignore
        return self  # type: ignore

    @classmethod
    async def connect(
        cls,
        conninfo: str = "",
        *,
        autocommit: bool = False,
        prepare_threshold: int | None = 5,
        context: AdaptContext | None = None,
        row_type: type[T] = tuple[Any, ...],
        validate: ValidationType = config.validation,
        strict: bool = config.strict,
        **kwargs: ConnParam,
    ) -> 'AsyncConnection[T]':

        return await super().connect(
            conninfo=conninfo,
            autocommit=autocommit,
            prepare_threshold=prepare_threshold,
            context=context,
            row_factory=cast(AsyncRowFactory[Row], get_row_factory(row_type, validate, strict)),
            cursor_factory=AsyncCursor,
            **kwargs,  # type: ignore
        )

    @overload
    def cursor(  # noqa
            self,
            name: Literal[""] = "",
    ) -> AsyncCursor[Row]: ...

    @overload
    def cursor(  # noqa
            self,
            name: str,
    ) -> AsyncServerCursor[Row]: ...

    def cursor(  # noqa
        self,
        name: str = "",
    ) -> AsyncCursor[Row] | AsyncServerCursor[Row]:

        return super().cursor(
            name=name,
        )  # type: ignore

    async def execute(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        prepare: bool | None = None,
        binary: bool = False,
    ) -> AsyncCursor[Row]:

        return await super().execute(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=params,
            prepare=prepare,
            binary=binary,
        )  # type: ignore
