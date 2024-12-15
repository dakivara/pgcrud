from msgspec import Struct


__all__ = ['Customer']


class Customer(Struct):
    id: int
    name: str
