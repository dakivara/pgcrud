from pgcrud.components import Select, InsertInto, Update, DeleteFrom
from pgcrud.types import DeleteFromValueType, SelectValueType, InsertIntoValueType, UpdateValueType


__all__ = ['QueryBuilder']


class QueryBuilder:

    def __new__(cls):
        raise TypeError("'QueryBuilder' object is not callable")

    @staticmethod
    def SELECT(value: SelectValueType) -> Select:
        return Select([], value)

    @staticmethod
    def INSERT_INTO(value: InsertIntoValueType) -> InsertInto:
        return InsertInto([], value)

    @staticmethod
    def UPDATE(value: UpdateValueType) -> Update:
        return Update([], value)

    @staticmethod
    def DELETE_FROM(value: DeleteFromValueType) -> DeleteFrom:
        return DeleteFrom([], value)
