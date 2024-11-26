from pgcrud.tab import SimpleTab


__all__ = [
    'TabGenerator',
]


class TabGeneratorType(type):

    def __getattr__(cls, name) -> SimpleTab:
        return SimpleTab(name)

    def __setattr__(cls, name, value):
        pass

    def __call__(cls, name) -> SimpleTab:
        return SimpleTab(name)


class TabGenerator(metaclass=TabGeneratorType):
    pass
