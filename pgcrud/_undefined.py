
__all__ = [
    'Undefined',
    'UndefinedType',
]


class UndefinedType(type):

    def __call__(cls):
        raise TypeError("'Undefined' object is not callable")

    def __str__(cls) -> str:
        return 'Undefined'

    def __repr__(cls) -> str:
        return cls.__str__()


class Undefined(metaclass=UndefinedType):
    pass
