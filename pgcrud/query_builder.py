from pgcrud.components import Select, InsertInto, Update, DeleteFrom
from pgcrud.types import DeleteFromValueType, SelectValueType, InsertIntoValueType, UpdateValueType


__all__ = ['QueryBuilder']


class QueryBuilder:

    def __new__(cls):
        raise TypeError("'QueryBuilder' object is not callable")

    @staticmethod
    def select(value: SelectValueType) -> Select:
        return Select([], value)

    @staticmethod
    def insert_into(value: InsertIntoValueType) -> InsertInto:
        return InsertInto([], value)

    @staticmethod
    def update(value: UpdateValueType) -> Update:
        return Update([], value)

    @staticmethod
    def delete_from(value: DeleteFromValueType) -> DeleteFrom:
        return DeleteFrom([], value)
