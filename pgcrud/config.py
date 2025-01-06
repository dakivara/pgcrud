from typing import TypedDict

import psycopg.types.json

from pgcrud.optional_dependencies import is_pydantic_installed, is_msgspec_installed, msgspec_json_dumps, msgspec_json_loads
from pgcrud.types import ValidationType


__all__ = [
    'ConfigDict',
    'config',
]


class Config:

    def __init__(
            self,
            validation: ValidationType = None,
            strict: bool = False,
    ):
        self._validation = validation
        self._strict = strict

    def __str__(self):
        return f'Config(validation={self.validation}, strict={self.strict})'

    def __repr__(self):
        return str(self)

    @property
    def validation(self) -> ValidationType:
        return self._validation  # type: ignore

    @validation.setter
    def validation(self, value: ValidationType):

        if value == 'pydantic':
            if not is_pydantic_installed:
                raise ValueError('Cannot set the value because pydantic is not installed.')

        elif value == 'msgspec':
            if not is_msgspec_installed:
                raise ValueError('Cannot set the value because msgspec is not installed.')

        self._validation = value

    @property
    def strict(self) -> bool:
        return self._strict

    @strict.setter
    def strict(self, value: bool) -> None:
        self._strict = value

    @staticmethod
    def set_json_loads(loads: psycopg.types.json.JsonLoadsFunction):
        psycopg.types.json.set_json_loads(loads)

    @staticmethod
    def set_json_dumps(dumps: psycopg.types.json.JsonDumpsFunction):
        psycopg.types.json.set_json_dumps(dumps)


class ConfigDict(TypedDict, total=False):
    validation: ValidationType
    strict: bool


config = Config()


if is_pydantic_installed:
    config.validation = 'pydantic'

elif is_msgspec_installed:
    config.validation = 'msgspec'
    config.set_json_dumps(msgspec_json_dumps)
    config.set_json_loads(msgspec_json_loads)
