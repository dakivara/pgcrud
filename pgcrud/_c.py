from pgcrud._col import SingleCol


__all__ = [
    'c',
]


class cMeta(type):

    def __getattr__(cls, name) -> SingleCol:
        return SingleCol(name, super().__getattribute__('_table_name'))

    def __setattr__(cls, name, value):
        pass

    def __call__(cls, name: str) -> SingleCol:
        return SingleCol(name)

    def __getitem__(cls, name) -> type:
        return type('c', (c,), {'_table_name': name})


class c(metaclass=cMeta):
    _table_name: str = None
