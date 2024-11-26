from abc import abstractmethod
from dataclasses import dataclass

from psycopg.sql import SQL, Composed


__all__ = ['Component']


@dataclass
class Component:
    prev_components: list['Component']

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    def __bool__(self):
        return len(self.get_single_composed()._obj) > 0

    @property
    def components(self) -> list['Component']:
        return self.prev_components + [self]

    @abstractmethod
    def get_single_composed(self) -> Composed:
        pass

    def get_composed(self) -> Composed:
        return SQL(' ').join([component.get_single_composed() for component in self.components if component])
