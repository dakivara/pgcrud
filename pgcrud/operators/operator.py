from abc import abstractmethod
from dataclasses import dataclass

from psycopg.sql import Composed


__all__ = ['Operator']


@dataclass
class Operator:

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def __bool__(self) -> bool:
        pass

    @abstractmethod
    def get_composed(self) -> Composed:
        pass
