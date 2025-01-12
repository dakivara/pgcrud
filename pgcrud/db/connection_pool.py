# pyright: reportIncompatibleMethodOverride=false, reportIncompatibleVariableOverride=false
from __future__ import annotations

from contextlib import contextmanager, asynccontextmanager
from typing import Any, AsyncIterator, Awaitable, Callable, Iterator

import psycopg_pool

from pgcrud.db.connection import Connection, AsyncConnection
from pgcrud.types import Row


__all__ = [
    'ConnectionPool',
    'AsyncConnectionPool',
]


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
