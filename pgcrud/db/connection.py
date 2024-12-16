# pyright: reportIncompatibleMethodOverride=false, reportIncompatibleVariableOverride=false

from contextlib import contextmanager, asynccontextmanager
from typing import Any, AsyncIterator, Awaitable, Callable, Iterator, Literal, cast, overload

import psycopg
from psycopg.abc import AdaptContext, ConnParam, Query, Params
from psycopg.pq.abc import PGconn
from psycopg.rows import RowFactory, AsyncRowFactory, tuple_row
import psycopg_pool

from pgcrud.config import config
from pgcrud.db.cursor import Cursor, ServerCursor, AsyncCursor, AsyncServerCursor
from pgcrud.db.shared import get_row_factory
from pgcrud.types import Row, T, ValidationType


__all__ = [
    'Connection',
    'ConnectionPool',
    'AsyncConnection',
    'AsyncConnectionPool',
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

    @classmethod
    def connect(
        cls,
        conninfo: str = "",
        *,
        autocommit: bool = False,
        prepare_threshold: int | None = 5,
        context: AdaptContext | None = None,
        row_type: type[T] = tuple[Any, ...],
        validate: ValidationType = config.validation_library,
        strict: bool = config.strict_validation,
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
    def cursor(
            self,
            name: Literal[""] = "",
    ) -> Cursor[Row]: ...

    @overload
    def cursor(
            self,
            name: str,
    ) -> ServerCursor[Row]: ...

    def cursor(
        self,
        name: str = "",
    ) -> Cursor[Row] | ServerCursor[Row]:

        return super().cursor(
            name=name,
        )  # type: ignore

    def execute(
        self,
        query: Query,
        params: Params | None = None,
        *,
        prepare: bool | None = None,
        binary: bool = False,
    ) -> Cursor[Row]:

        return super().execute(
            query=query,
            params=params,
            prepare=prepare,
            binary=binary,
        )  # type: ignore


class ConnectionPool(psycopg_pool.ConnectionPool[Row]):  # type: ignore

    connection_class: type[Connection[Row]]

    def __init__(
        self,
        conninfo: str = "",
        *,
        kwargs: dict[str, Any] | None = None,
        min_size: int = 4,
        max_size: int | None = None,
        open: bool | None = None,
        configure: Callable[[Connection[Row]], None] | None = None,
        check: Callable[[Connection[Row]], None] | None = None,
        reset: Callable[[Connection[Row]], None] | None = None,
        name: str | None = None,
        timeout: float = 30.0,
        max_waiting: int = 0,
        max_lifetime: float = 60 * 60.0,
        max_idle: float = 10 * 60.0,
        reconnect_timeout: float = 5 * 60.0,
        reconnect_failed: Callable[['ConnectionPool[Row]'], None] | None = None,
        num_workers: int = 3,
    ):
        super().__init__(
            conninfo=conninfo,
            connection_class=Connection,  # type: ignore
            kwargs=kwargs,
            min_size=min_size,
            max_size=max_size,
            open=open,
            configure=configure,  # type: ignore
            check=check,  # type: ignore
            reset=reset,  # type: ignore
            name=name,
            timeout=timeout,
            max_waiting=max_waiting,
            max_lifetime=max_lifetime,
            max_idle=max_idle,
            reconnect_timeout=reconnect_timeout,
            reconnect_failed=reconnect_failed,  # type: ignore
            num_workers=num_workers,
        )

    @contextmanager
    def connection(self, timeout: float | None = None) -> Iterator[Connection[Row]]:
        with super().connection(timeout=timeout) as conn:
            yield conn  # type: ignore

    def getconn(self, timeout: float | None = None) -> Connection[Row]:
        return super().getconn(timeout)  # type: ignore

    def putconn(self, conn: Connection[Row]) -> None:
        super().putconn(conn)  # type: ignore

    @staticmethod
    def check_connection(conn: Connection[Row]) -> None:
        psycopg_pool.ConnectionPool.check_connection(conn)  # type: ignore


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

    @classmethod
    async def connect(
        cls,
        conninfo: str = "",
        *,
        autocommit: bool = False,
        prepare_threshold: int | None = 5,
        context: AdaptContext | None = None,
        row_type: type[T] = tuple[Any, ...],
        validate: ValidationType = config.validation_library,
        strict: bool = config.strict_validation,
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
    def cursor(
            self,
            name: Literal[""] = "",
    ) -> AsyncCursor[Row]: ...

    @overload
    def cursor(
            self,
            name: str,
    ) -> AsyncServerCursor[Row]: ...

    def cursor(
        self,
        name: str = "",
    ) -> AsyncCursor[Row] | AsyncServerCursor[Row]:

        return super().cursor(
            name=name,
        )  # type: ignore

    async def execute(
        self,
        query: Query,
        params: Params | None = None,
        *,
        prepare: bool | None = None,
        binary: bool = False,
    ) -> AsyncCursor[Row]:

        return await super().execute(
            query=query,
            params=params,
            prepare=prepare,
            binary=binary,
        )  # type: ignore


class AsyncConnectionPool(psycopg_pool.AsyncConnectionPool[Row]):  # type: ignore

    connection_class: type[AsyncConnection[Row]]

    def __init__(
        self,
        conninfo: str = "",
        *,
        kwargs: dict[str, Any] | None = None,
        min_size: int = 4,
        max_size: int | None = None,
        open: bool | None = None,
        configure: Callable[[AsyncConnection[Row]], Awaitable[None]] | None = None,
        check: Callable[[AsyncConnection[Row]], Awaitable[None]] | None = None,
        reset: Callable[[AsyncConnection[Row]], Awaitable[None]] | None = None,
        name: str | None = None,
        timeout: float = 30.0,
        max_waiting: int = 0,
        max_lifetime: float = 60 * 60.0,
        max_idle: float = 10 * 60.0,
        reconnect_timeout: float = 5 * 60.0,
        reconnect_failed: Callable[['AsyncConnectionPool[Row]'], Awaitable[None]] | None = None,
        num_workers: int = 3,
    ):
        super().__init__(
            conninfo=conninfo,
            connection_class=AsyncConnection,  # type: ignore
            kwargs=kwargs,
            min_size=min_size,
            max_size=max_size,
            open=open,
            configure=configure,  # type: ignore
            check=check,  # type: ignore
            reset=reset,  # type: ignore
            name=name,
            timeout=timeout,
            max_waiting=max_waiting,
            max_lifetime=max_lifetime,
            max_idle=max_idle,
            reconnect_timeout=reconnect_timeout,
            reconnect_failed=reconnect_failed,  # type: ignore
            num_workers=num_workers,
        )

    @asynccontextmanager
    async def connection(self, timeout: float | None = None) -> AsyncIterator[AsyncConnection[Row]]:
        async with super().connection(timeout=timeout) as conn:
            yield conn  # type: ignore

    async def getconn(self, timeout: float | None = None) -> AsyncConnection[Row]:
        return await super().getconn(timeout)  # type: ignore

    async def putconn(self, conn: AsyncConnection[Row]) -> None:
        await super().putconn(conn)  # type: ignore

    @staticmethod
    async def check_connection(conn: AsyncConnection[Row]) -> None:
        await psycopg_pool.AsyncConnectionPool.check_connection(conn)  # type: ignore
