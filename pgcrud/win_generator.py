from pgcrud.win import Win


__all__ = ['WinGenerator']


class WinGeneratorType(type):

    def __getattr__(cls, name) -> Win:
        return Win(name)

    def __setattr__(cls, name, value):
        pass

    def __call__(cls, name) -> Win:
        return Win(name)


class WinGenerator(metaclass=WinGeneratorType):
    pass
