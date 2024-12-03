from typing import Any
from pgcrud.clauses import From, Select, Where, GroupBy, Having, OrderBy, Limit, Offset, InsertInto, Values, Update, Set, DeleteFrom, Using
from pgcrud.query import Query
from pgcrud.types import DeleteFromValueType, FromValueType, GroupByValueType, HavingValueType, InsertIntoValueType, OrderByValueType, SelectValueType, SetColsType, SetValuesType, UpdateValueType, UsingValueType, ValuesValueType, WhereValueType


__all__ = ['QueryBuilder']


class QueryBuilder:

    def __new__(cls):
        raise TypeError("'QueryBuilder' object is not callable")

    @staticmethod
    def SELECT(value: SelectValueType) -> Query:
        return Query([Select(value)])

    @staticmethod
    def FROM(value: FromValueType) -> Query:
        return Query([From(value)])

    @staticmethod
    def WHERE(value: WhereValueType) -> Query:
        return Query([Where(value)])

    @staticmethod
    def GROUP_BY(value: GroupByValueType) -> Query:
        return Query([GroupBy(value)])

    @staticmethod
    def HAVING(value: HavingValueType) -> 'Query':
        return Query([Having(value)])

    @staticmethod
    def ORDER_BY(value: OrderByValueType) -> 'Query':
        return Query([OrderBy(value)])

    @staticmethod
    def LIMIT(value: int) -> 'Query':
        return Query([Limit(value)])

    @staticmethod
    def OFFSET(value: int) -> 'Query':
        return Query([Offset(value)])

    @staticmethod
    def INSERT_INTO(value: InsertIntoValueType) -> 'Query':
        return Query([InsertInto(value)])

    @staticmethod
    def VALUES(*args: ValuesValueType, **kwargs: Any) -> 'Query':
        return Query([Values(args, kwargs)])

    @staticmethod
    def UPDATE(value: UpdateValueType) -> 'Query':
        return Query([Update(value)])

    @staticmethod
    def SET(cols: SetColsType, values: SetValuesType, **kwargs: Any) -> 'Query':
        return Query([Set(cols, values, kwargs)])

    @staticmethod
    def DELETE_FROM(value: DeleteFromValueType) -> 'Query':
        return Query([DeleteFrom(value)])

    @staticmethod
    def USING(value: UsingValueType) -> 'Query':
        return Query([Using(value)])
