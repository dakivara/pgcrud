from pgcrud._tab import Tab


__all__ = [
    't',
]


class tMeta(type):

    def __getattr__(cls, name) -> Tab:
        return Tab(name)

    def __setattr__(cls, name, value):
        pass

    def __call__(cls, name) -> Tab:
        return Tab(name)


class t(metaclass=tMeta):
    pass
