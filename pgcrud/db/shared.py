from types import GenericAlias, UnionType
from typing import Annotated, Any, get_args, get_origin
from psycopg.rows import BaseRowFactory, scalar_row, tuple_row, dict_row, class_row, args_row, kwargs_row

from pgcrud.config import ConfigDict, config
from pgcrud.optional_dependencies import (
    is_pydantic_installed,
    is_pydantic_model,
    is_msgspec_installed,
    is_msgspec_model,
    msgspec_kwargs_fun_generator,
    pydantic_kwargs_fun_generator,
    pydantic_args_fun_generator,
    msgspec_args_fun_generator,
    pydantic_scalar_row_generator,
    msgspec_scalar_row_generator,
    pydantic_to_dict,
    msgspec_to_dict,
    is_pydantic_instance,
    is_msgspec_instance,
)
from pgcrud.types import T, ValidationType


__all__ = [
    'deserialize_params',
    'get_params',
    'get_row_factory',
]


def deserialize_params(params: Any) -> Any:
    if is_pydantic_installed and is_pydantic_instance(params):
        return pydantic_to_dict(params)  # type: ignore
    elif is_msgspec_installed and is_msgspec_instance(params):
        return msgspec_to_dict(params)  # type: ignore
    else:
        return params


def get_params(item: type[T] | tuple[type[T], ConfigDict]) -> tuple[type[T], ValidationType, bool]:

    if isinstance(item, tuple):
        row_type = item[0]
        config_dict = item[1]
    else:
        row_type = item
        config_dict: ConfigDict = {}

    validate = config_dict.get('validation') or config.validation
    strict = config_dict.get('strict') or config.strict

    return row_type, validate, strict


def extract_origin(row_type: Any) -> type:

    if get_origin(row_type) is Annotated:
        return extract_origin(get_args(row_type)[0])
    else:
        if isinstance(row_type, UnionType):
            return extract_origin(get_args(row_type)[0])
        elif isinstance(row_type, GenericAlias):
            return extract_origin(get_origin(row_type))
        else:
            return row_type


def get_row_factory(row_type: type[T], validate: ValidationType, strict: bool) -> BaseRowFactory[T]:

    origin = extract_origin(row_type)

    if is_msgspec_installed and is_msgspec_model(origin):
        if validate == 'pydantic':
            return kwargs_row(pydantic_kwargs_fun_generator(row_type, strict))
        elif validate == 'msgspec':
            return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
        else:
            # always validates because it is the only way to construct the model recursively
            return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))

    elif is_pydantic_installed and is_pydantic_model(origin):
        if validate == 'pydantic':
            return class_row(row_type)
        elif validate == 'msgspec':
            return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
        else:
            # always validates because it is the only way to construct the model recursively
            return class_row(row_type) # type: ignore

    elif issubclass(origin, dict):
        if validate == 'pydantic':
            return kwargs_row(pydantic_kwargs_fun_generator(row_type, strict))
        elif validate == 'msgspec':
            return kwargs_row(msgspec_kwargs_fun_generator(row_type, strict))
        else:
            return dict_row  # type: ignore

    elif issubclass(origin, list):
        if validate == 'pydantic':
            return args_row(pydantic_args_fun_generator(row_type, strict))
        elif validate == 'msgspec':
            return args_row(msgspec_args_fun_generator(row_type, strict))
        else:
            return args_row(list)  # type: ignore

    elif issubclass(origin, tuple):
        if validate == 'pydantic':
            return args_row(pydantic_args_fun_generator(row_type, strict))
        elif validate == 'msgspec':
            return args_row(msgspec_args_fun_generator(row_type, strict))
        else:
            return tuple_row  # type: ignore

    elif issubclass(origin, set):
        if validate == 'pydantic':
            return args_row(pydantic_args_fun_generator(row_type, strict))
        elif validate == 'msgspec':
            return args_row(msgspec_args_fun_generator(row_type, strict))
        else:
            return args_row(set)  # type: ignore

    else:
        if validate == 'pydantic':
            return pydantic_scalar_row_generator(row_type, strict)
        elif validate == 'msgspec':
            return msgspec_scalar_row_generator(row_type, strict)
        else:
            return scalar_row
