import psycopg

from pgcrud.config import ConfigDict
from pgcrud.db.shared import T, get_params, get_row_factory
from pgcrud.types import Row


__all__ = [
    'Cursor',
    'ServerCursor',
    'AsyncCursor',
    'AsyncServerCursor',
]


class Cursor(psycopg.Cursor[Row]):

    def __getitem__(self, item: type[T] | tuple[type[T], ConfigDict]) -> 'Cursor[T]':
        type_, validate, strict = get_params(item)
        self.row_factory = get_row_factory(type_, validate, strict)  # type: ignore
        return self  # type: ignore


class ServerCursor(psycopg.ServerCursor[Row]):

    def __getitem__(self, item: type[T] | tuple[type[T], ConfigDict]) -> 'ServerCursor[T]':
        type_, validate, strict = get_params(item)
        self.row_factory = get_row_factory(type_, validate, strict)  # type: ignore

        return self  # type: ignore


class AsyncCursor(psycopg.AsyncCursor[Row]):

    def __getitem__(self, item: type[T] | tuple[type[T], ConfigDict]) -> 'AsyncCursor[T]':
        type_, validate, strict = get_params(item)
        self.row_factory = get_row_factory(type_, validate, strict)  # type: ignore
        return self  # type: ignore


class AsyncServerCursor(psycopg.AsyncServerCursor[Row]):

    def __getitem__(self, item: type[T] | tuple[type[T], ConfigDict]) -> 'AsyncServerCursor[T]':
        type_, validate, strict = get_params(item)
        self.row_factory = get_row_factory(type_, validate, strict)  # type: ignore
        return self  # type: ignore
