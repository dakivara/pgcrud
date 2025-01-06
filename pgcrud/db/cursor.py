# pyright: reportIncompatibleMethodOverride=false, reportIncompatibleVariableOverride=false

from typing import Any, Iterable, Iterator, Sequence, AsyncIterator

import psycopg

from pgcrud.config import ConfigDict
from pgcrud.db.shared import deserialize_params, get_params, get_row_factory
from pgcrud.query import Query
from pgcrud.types import ParamsType, QueryType, Row, T


__all__ = [
    'Cursor',
    'ServerCursor',
    'AsyncCursor',
    'AsyncServerCursor',
]


class Cursor(psycopg.Cursor[Row]):

    def __getitem__(
            self,
            item: type[T] | tuple[type[T], ConfigDict],
    ) -> 'Cursor[T]':
        row_type, validate, strict = get_params(item)
        self.row_factory = get_row_factory(row_type, validate, strict)  # type: ignore
        return self  # type: ignore

    def execute(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        prepare: bool | None = None,
        binary: bool | None = None,
    ) -> 'Cursor[Row]':

        return super().execute(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=deserialize_params(params),
            prepare=prepare,
            binary=binary,
        )

    def executemany(
        self,
        query: QueryType,
        params_seq: Sequence[ParamsType],
        *,
        returning: bool = False
    ) -> None:

        super().executemany(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params_seq=[deserialize_params(params) for params in params_seq],
            returning=returning,
        )

    def stream(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        binary: bool | None = None,
        size: int = 1,
    ) -> Iterator[Row]:

        return super().stream(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=deserialize_params(params),
            binary=binary,
            size=size,
        )


class ServerCursor(psycopg.ServerCursor[Row]):

    def __getitem__(
            self,
            item: type[T] | tuple[type[T], ConfigDict],
    ) -> 'ServerCursor[T]':

        row_type, validate, strict = get_params(item)
        self.row_factory = get_row_factory(row_type, validate, strict)  # type: ignore
        return self  # type: ignore

    def execute(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        binary: bool | None = None,
        **kwargs: Any,
    ) -> 'ServerCursor[Row]':

        return super().execute(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=deserialize_params(params),
            binary=binary,
            **kwargs,
        )

    def executemany(
        self,
        query: QueryType,
        params_seq: Iterable[ParamsType],
        *,
        returning: bool = True,
    ) -> None:

        super().executemany(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params_seq=[deserialize_params(params) for params in params_seq],
            returning=returning,
        )

    def stream(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        binary: bool | None = None,
        size: int = 1,
    ) -> Iterator[Row]:

        return super().stream(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=deserialize_params(params),
            binary=binary,
            size=size,
        )


class AsyncCursor(psycopg.AsyncCursor[Row]):

    def __getitem__(self, item: type[T] | tuple[type[T], ConfigDict]) -> 'AsyncCursor[T]':
        row_type, validate, strict = get_params(item)
        self.row_factory = get_row_factory(row_type, validate, strict)  # type: ignore
        return self  # type: ignore

    async def execute(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        prepare: bool | None = None,
        binary: bool | None = None,
    ) -> 'AsyncCursor[Row]':

        return await super().execute(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=deserialize_params(params),
            prepare=prepare,
            binary=binary,
        )

    async def executemany(
        self,
        query: QueryType,
        params_seq: Iterable[ParamsType],
        *,
        returning: bool = False,
    ) -> None:

        await super().executemany(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params_seq=[deserialize_params(params) for params in params_seq],
            returning=returning,
        )

    async def stream(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        binary: bool | None = None,
        size: int = 1,
    ) -> AsyncIterator[Row]:

        return super().stream(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=deserialize_params(params),
            binary=binary,
            size=size,
        )


class AsyncServerCursor(psycopg.AsyncServerCursor[Row]):

    def __getitem__(self, item: type[T] | tuple[type[T], ConfigDict]) -> 'AsyncServerCursor[T]':
        row_type, validate, strict = get_params(item)
        self.row_factory = get_row_factory(row_type, validate, strict)  # type: ignore
        return self  # type: ignore

    async def execute(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        binary: bool | None = None,
        **kwargs: Any,
    ) -> 'AsyncServerCursor[Row]':

        return await super().execute(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=deserialize_params(params),
            binary=binary,
            **kwargs,
        )

    async def executemany(
        self,
        query: QueryType,
        params_seq: Iterable[ParamsType],
        *,
        returning: bool = True,
    ) -> None:

        await super().executemany(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params_seq=[deserialize_params(params) for params in params_seq],
            returning=returning,
        )

    async def stream(
        self,
        query: QueryType,
        params: ParamsType | None = None,
        *,
        binary: bool | None = None,
        size: int = 1,
    ) -> AsyncIterator[Row]:

        return super().stream(
            query=str(query) if isinstance(query, Query) else query,  # type: ignore
            params=deserialize_params(params),
            binary=binary,
            size=size,
        )
