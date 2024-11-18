from abc import abstractmethod
from dataclasses import dataclass

from psycopg.sql import SQL, Composed


__all__ = [
    'LogicalOperator',
    'And',
    'Or',
]


@dataclass
class LogicalOperator:
    operators: list['FilterOperator | LogicalOperator']

    @abstractmethod
    def get_composed(self) -> Composed | None:
        pass


class And(LogicalOperator):

    def get_composed(self) -> Composed | None:
        composed_list = [composed for operator in self.operators if (composed := operator.get_composed(True))]
        if composed_list:
            composed = SQL(' AND ').join(composed_list)
            if len(composed_list) > 1:
                composed = Composed([SQL('('), composed, SQL(')')])
            return composed


class Or(LogicalOperator):

    def get_composed(self) -> Composed | None:
        composed_list = [composed for operator in self.operators if (composed := operator.get_composed(True))]
        if composed_list:
            composed = SQL(' OR ').join(composed_list)
            if len(composed_list) > 1:
                composed = Composed([SQL('('), composed, SQL(')')])
            return composed
