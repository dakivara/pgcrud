from typing import Any, TYPE_CHECKING

from pgcrud.col import make_col, AvgCol, SumCol, ToJsonCol, JsonAggCol, CoalesceCol

if TYPE_CHECKING:
    from pgcrud.col import Col
    from pgcrud.tab import Tab


__all__ = ['FunctionBearer']


class FunctionBearer:

    def __new__(cls):
        raise TypeError("'FunctionBearer' object is not callable")

    @staticmethod
    def sum(col: 'Col') -> SumCol:
        return SumCol(col)

    @staticmethod
    def avg(col: 'Col') -> AvgCol:
        return AvgCol(col)

    @staticmethod
    def json_agg(value: 'Tab | Col') -> JsonAggCol:
        return JsonAggCol(value)

    @staticmethod
    def coalesce(*args: Any) -> CoalesceCol:
        return CoalesceCol([make_col(arg) for arg in args])

    @staticmethod
    def to_json(tab: 'Tab') -> ToJsonCol:
        return ToJsonCol(tab)
