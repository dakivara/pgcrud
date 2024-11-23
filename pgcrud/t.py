from pgcrud.tab import SimpleTab


__all__ = [
    't',
]


class tMeta(type):

    def __getattr__(cls, name) -> SimpleTab:
        return SimpleTab(name)

    def __setattr__(cls, name, value):
        pass

    def __call__(cls, name) -> SimpleTab:
        return SimpleTab(name)


class t(metaclass=tMeta):
    pass
