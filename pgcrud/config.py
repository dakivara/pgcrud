from dataclasses import dataclass
from typing import TypedDict

import psycopg.types.json

from pgcrud.optional_dependencies import is_pydantic_installed, is_msgspec_installed
from pgcrud.types import ValidationType


__all__ = [
    'ConfigDict',
    'config',
]


@dataclass
class Config:
    _validation_library: ValidationType = None
    _strict_validation: bool = False

    def __str__(self):
        return f'Config(validation_library={self.validation_library}, strict_validation={self.strict_validation})'

    def __repr__(self):
        return str(self)

    @property
    def validation_library(self) -> ValidationType:
        return self._validation_library

    @validation_library.setter
    def validation_library(self, value: ValidationType):

        if value == 'pydantic':
            if not is_pydantic_installed:
                raise ValueError('Cannot set the value because pydantic is not installed.')

        elif value == 'msgspec':
            if not is_msgspec_installed:
                raise ValueError('Cannot set the value because msgspec is not installed.')

        self._validation_library = value

    @property
    def strict_validation(self) -> bool:
        return self._strict_validation

    @strict_validation.setter
    def strict_validation(self, value: bool) -> None:
        self._strict_validation = value

    def set_json_loads(self, loads: psycopg.types.json.JsonLoadsFunction):
        psycopg.types.json.set_json_loads(loads)

    def set_json_dumps(self, dumps: psycopg.types.json.JsonDumpsFunction):
        psycopg.types.json.set_json_dumps(dumps)


class ConfigDict(TypedDict, total=False):
    validation_library: ValidationType
    strict_validation: bool


config = Config()
