from collections.abc import Sequence
from typing import Any, TypeVar

from psycopg._cursor_base import BaseCursor
from psycopg import errors as e
from psycopg.rows import BaseRowFactory, RowMaker, no_result, _get_names, _get_nfields
from pydantic import TypeAdapter


__all__ = [
    'scalar_row',
    'tuple_row',
    'dict_row',
]


T = TypeVar('T', bound=tuple)
D = TypeVar('D', bound=dict)


def scalar_row(type_: type[Any]) -> BaseRowFactory[Any]:

    ta = TypeAdapter(type_)

    def scalar_row_(cursor: BaseCursor[Any, Any]) -> RowMaker[Any]:

        res = cursor.pgresult
        if not res:
            return no_result

        nfields = _get_nfields(res)
        if nfields is None:
            return no_result

        if nfields < 1:
            raise e.ProgrammingError("at least one column expected")

        def scalar_row__(values: Sequence[Any]) -> Any:
            return ta.validate_python(values[0])

        return scalar_row__

    return scalar_row_


def tuple_row(type_: type[T]) -> BaseRowFactory[T]:

    ta = TypeAdapter(type_)

    def tuple_row_(cursor: BaseCursor[Any, Any]) -> RowMaker[T]:

        def tuple_row__(values: Sequence[Any]) -> T:
            return ta.validate_python(tuple(values))

        return tuple_row__

    return tuple_row_


def dict_row(type_: type[D]) -> BaseRowFactory[D]:

    ta = TypeAdapter(type_)

    def dict_row_(cursor: BaseCursor[Any, Any]) -> RowMaker[D]:

        names = _get_names(cursor)
        if names is None:
            return no_result

        def dict_row__(values: Sequence[Any]) -> D:
            return ta.validate_python(dict(zip(names, values)))

        return dict_row__

    return dict_row_
