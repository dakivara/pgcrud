
__all__ = [
    'Undefined',
    'UndefinedType',
]


class UndefinedType(type):

    def __call__(cls):
        raise TypeError("'Undefined' object is not callable")


class Undefined(metaclass=UndefinedType):
    pass
