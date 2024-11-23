from typing import TYPE_CHECKING

from pgcrud._col import SingleCol

if TYPE_CHECKING:
    from pgcrud._tab import Tab


__all__ = [
    'c',
]


class cMeta(type):

    def __getattr__(cls, name) -> SingleCol:
        return SingleCol(name, super().__getattribute__('_table'))

    def __setattr__(cls, name, value):
        pass

    def __call__(cls, name: str) -> SingleCol:
        return SingleCol(name)

    def __getitem__(cls, table: 'Tab') -> type:
        return type('c', (c,), {'_table': table})


class c(metaclass=cMeta):
    _table: 'Tab | None' = None
