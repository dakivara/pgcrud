from pgcrud.components import Select, InsertInto
from pgcrud.components.update import Update
from pgcrud.types import SelectValueType, InsertIntoValueType, UpdateValueType


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
