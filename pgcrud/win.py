from dataclasses import dataclass

from psycopg.sql import SQL, Composed, Identifier


__all__ = ['Win']


@dataclass
class Win:
    name: str

    def __str__(self):
        return self.get_composed().as_string()

    def __repr__(self):
        return self.__str__()

    def get_composed(self) -> Composed:
        return SQL('{}').format(Identifier(self.name))

    def as_(self) -> None:
        pass
