from types import GenericAlias
from typing import Any, TypeVar

import msgspec
from psycopg.rows import BaseRowFactory, scalar_row, tuple_row, dict_row, class_row, args_row, kwargs_row

from pgcrud.optional_dependencies import is_pydantic_installed
from pgcrud.types import T


__all__ = [
    'get_params',
    'get_row_factory',
]


def is_generic_alias(type_: Any) -> bool:
    return isinstance(type_, GenericAlias)


def is_pydantic_model(type_: type) -> bool:
    from pydantic import BaseModel
    return not is_generic_alias(type_) and issubclass(type_, BaseModel)


def get_params(item: type[T] | tuple[type[T]] | tuple[type[T], bool] | tuple[type[T], bool, bool]) -> tuple[type[T], bool, bool]:

    if not isinstance(item, tuple):
        item = (item, False, False)
    elif len(item) == 1:
        item += (False, False)
    elif len(item) == 2:
        item += (False,)

    type_, validate, strict = item
    type_: type[T]  # Pyright is not correctly inferring the type

    return type_, validate, strict


def get_row_factory(type_: type[T], validate: bool, strict: bool) -> BaseRowFactory[Any]:

    if issubclass(type_, msgspec.Struct):
        if validate:
            return kwargs_row(lambda **kwargs: msgspec.convert(kwargs, type=type_, strict=strict))
        else:
            return class_row(type_)

    elif is_pydantic_installed and is_pydantic_model(type_):
        if validate:
            return class_row(type_)  # type: ignore
        else:
            return kwargs_row(type_.model_construct)  # type: ignore

    elif issubclass(getattr(type_, '__origin__', type_), dict):
        if validate:
            return kwargs_row(lambda **kwargs: msgspec.convert(kwargs, type=type_, strict=strict))
        else:
            return dict_row

    elif issubclass(getattr(type_, '__origin__', type_), tuple):
        if validate:
            return args_row(lambda *args: msgspec.convert(args, type=type_, strict=strict))
        else:
            return tuple_row

    else:
        if validate:
            return args_row(lambda *args: msgspec.convert(args[0], type=type_, strict=strict))
        else:
            return scalar_row
