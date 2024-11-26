from typing import TYPE_CHECKING

from pgcrud.col import SingleCol

if TYPE_CHECKING:
    from pgcrud.tab import Tab


__all__ = [
    'ColGenerator',
]


class ColGeneratorType(type):

    def __getattr__(cls, name) -> SingleCol:
        return SingleCol(name, super().__getattribute__('_table'))

    def __setattr__(cls, name, value):
        pass

    def __call__(cls, name: str) -> SingleCol:
        return SingleCol(name)

    def __getitem__(cls, table: 'Tab') -> type:
        return type('ColGenerator', (ColGenerator,), {'_table': table})


class ColGenerator(metaclass=ColGeneratorType):
    _table: 'Tab | None' = None
