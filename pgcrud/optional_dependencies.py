# pyright: reportPossiblyUnboundVariable=false, reportMissingImports=false

from collections.abc import Sequence
import importlib.util
from typing import Any, Callable

from psycopg._cursor_base import BaseCursor
from psycopg.rows import BaseRowFactory, RowMaker, scalar_row


is_pydantic_installed =  bool(importlib.util.find_spec('pydantic'))
is_msgspec_installed = bool(importlib.util.find_spec('msgspec'))

if is_pydantic_installed:
    from pydantic import BaseModel as PydanticModel, TypeAdapter as PydanticTypeAdapter

if is_msgspec_installed:
    from msgspec import Struct as MsgspecModel, to_builtins as msgspec_to_builtins, convert as msgspec_convert
    from msgspec.json import encode as msgspec_encode, decode as msgspec_decode


__all__ = [
    'is_pydantic_installed',
    'is_pydantic_model',
    'is_pydantic_instance',
    'pydantic_to_dict',
    'pydantic_kwargs_fun_generator',
    'pydantic_args_fun_generator',
    'pydantic_scalar_row_generator',

    'is_msgspec_installed',
    'is_msgspec_model',
    'is_msgspec_instance',
    'msgspec_to_dict',
    'msgspec_kwargs_fun_generator',
    'msgspec_args_fun_generator',
    'msgspec_scalar_row_generator',
    'msgspec_json_dumps',
    'msgspec_json_loads',
]


pydantic_type_adapters: dict[type, 'PydanticTypeAdapter'] = {}


def is_pydantic_model(type_: type) -> bool:
    return issubclass(type_, PydanticModel)


def is_msgspec_model(type_: type) -> bool:
    return issubclass(type_, MsgspecModel)


def is_pydantic_instance(value: Any) -> bool:
    return isinstance(value, PydanticModel)


def is_msgspec_instance(value: Any) -> bool:
    return isinstance(value, MsgspecModel)


def pydantic_to_dict(value: 'PydanticModel') -> dict[str, Any]:
    return value.model_dump(by_alias=True)


def msgspec_to_dict(value: 'MsgspecModel') -> dict[str, Any]:
    return msgspec_to_builtins(value)


def pydantic_kwargs_fun_generator(row_type: type, strict: bool) -> Callable[..., Any]:

    ta = pydantic_type_adapters.get(row_type) or PydanticTypeAdapter(row_type)

    def kwargs_fun(**kwargs: Any) -> Any:
        return ta.validate_python(kwargs, strict=strict)

    return kwargs_fun


def msgspec_kwargs_fun_generator(row_type: type, strict: bool) -> Callable[..., Any]:

    def kwargs_fun(**kwargs: Any) -> Any:
        return msgspec_convert(kwargs, type=row_type, strict=strict)

    return kwargs_fun


def pydantic_args_fun_generator(row_type: type, strict: bool) -> Callable[..., Any]:

    ta = pydantic_type_adapters.get(row_type) or PydanticTypeAdapter(row_type)

    def args_fun(*args: Any) -> Any:
        return ta.validate_python(args, strict=strict)

    return args_fun


def msgspec_args_fun_generator(row_type: type, strict: bool) -> Callable[..., Any]:

    def args_fun(*args: Any) -> Any:
        return msgspec_convert(args, type=row_type, strict=strict)

    return args_fun


def pydantic_scalar_row_generator(row_type: type, strict: bool) -> BaseRowFactory[Any]:

    ta = pydantic_type_adapters.get(row_type) or PydanticTypeAdapter(row_type)

    def pydantic_scalar_row(cursor: BaseCursor[Any, Any]) -> RowMaker[Any]:
        scalar_row(cursor)

        def pydantic_scalar_row_(values: Sequence[Any]) -> Any:
            return ta.validate_python(values[0], strict=strict)

        return pydantic_scalar_row_

    return pydantic_scalar_row


def msgspec_scalar_row_generator(row_type: type, strict: bool) -> BaseRowFactory[Any]:

    def msgspec_scalar_row(cursor: BaseCursor[Any, Any]) -> RowMaker[Any]:
        scalar_row(cursor)

        def msgspec_scalar_row_(values: Sequence[Any]) -> Any:
            return msgspec_convert(values[0], type=row_type, strict=strict)

        return msgspec_scalar_row_

    return msgspec_scalar_row


def msgspec_json_dumps(obj: Any) -> bytes:
    return msgspec_encode(obj)


def msgspec_json_loads(buf: bytes | str) -> Any:
    return msgspec_decode(buf)
