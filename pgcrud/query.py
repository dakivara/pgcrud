from dataclasses import dataclass
from typing import TYPE_CHECKING

from psycopg.sql import SQL, Composed


if TYPE_CHECKING:
    from pgcrud.components import Component


__all__ = ['Query']


@dataclass
class Query:
    component: 'Component'

    def get_composed(self) -> Composed:
        return self.component.get_composed()
