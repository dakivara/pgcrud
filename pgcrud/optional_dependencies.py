import importlib.util
from types import GenericAlias
from typing import Any


__all__ = [
    'is_pydantic_installed',
    'is_pydantic_model',
    'is_pydantic_instance',
]


def is_generic_alias(type_: Any) -> bool:
    return isinstance(type_, GenericAlias)


is_pydantic_installed =  bool(importlib.util.find_spec('pydantic'))


def is_pydantic_model(type_: type) -> bool:
    from pydantic import BaseModel
    return not is_generic_alias(type_) and issubclass(type_, BaseModel)


def is_pydantic_instance(value: Any) -> bool:
    from pydantic import BaseModel
    return isinstance(value, BaseModel)
