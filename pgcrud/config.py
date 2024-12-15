from dataclasses import dataclass
from typing import Literal

from pgcrud.optional_dependencies import is_pydantic_installed, is_msgspec_installed


__all__ = ['config']


@dataclass
class Config:
    _validation_library: Literal['pydantic', 'msgspec', None] = None
    _validation_default: bool = False
    _strict_default: bool = False

    def __str__(self):
        return f'Config(validation_library={self.validation_library}, validation_default={self.validation_default}, strict_default={self._strict_default})'

    def __repr__(self):
        return str(self)

    @property
    def validation_library(self) -> Literal['pydantic', 'msgspec', None]:
        return self._validation_library

    @validation_library.setter
    def validation_library(self, value: Literal['pydantic', 'msgspec', None]):

        if value == 'pydantic':
            if not is_pydantic_installed:
                raise ValueError('Cannot set the value because pydantic is not installed.')

        elif value == 'msgspec':
            if not is_msgspec_installed:
                raise ValueError('Cannot set the value because msgspec is not installed.')

        self._validation_library = value

    @property
    def validation_default(self) -> bool:
        return self._validation_default

    @validation_default.setter
    def validation_default(self, value: bool) -> None:
        self._validation_default = value

    @property
    def strict_default(self) -> bool:
        return self._strict_default

    @strict_default.setter
    def strict_default(self, value: bool) -> None:
        self._strict_default = value


config = Config()


if is_pydantic_installed:
    config.validation_library = 'pydantic'
elif is_msgspec_installed:
    config.validation_library = 'msgspec'
