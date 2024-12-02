from abc import abstractmethod
from dataclasses import dataclass

from psycopg.sql import Composed


__all__ = [
    'Operator',
    'UndefinedOperator',
]


@dataclass
class Operator:

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return not isinstance(self, UndefinedOperator)

    @abstractmethod
    def get_composed(self) -> Composed:
        pass


@dataclass(repr=False)
class UndefinedOperator(Operator):

    def get_composed(self) -> Composed:
        return Composed([])
