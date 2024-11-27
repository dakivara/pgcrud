from collections.abc import Sequence

from psycopg.sql import Composed
from psycopg.rows import scalar_row, tuple_row, class_row, RowFactory, AsyncRowFactory

from pgcrud.col import Col
from pgcrud.query_builder import QueryBuilder as q
from pgcrud.types import DeleteFromValueType, GroupByValueType, HavingValueType, SelectValueType, FromValueType, JoinValueType, SetColsType, SetValueType, UpdateValueType, UsingValueType, WhereValueType, OrderByValueType, InsertIntoValueType, ValuesValueType, ReturningValueType, AdditionalValuesType


__all__ = [
    'get_row_factory',
    'get_async_row_factory',
    'construct_composed_get_query',
    'construct_composed_insert_query',
    'construct_composed_update_query',
    'construct_composed_delete_query',
]


def get_row_factory(select: SelectValueType) -> RowFactory:
    if isinstance(select, Col):
        return scalar_row
    elif isinstance(select, Sequence):
        return tuple_row
    else:
        return class_row(select)  # type: ignore


def get_async_row_factory(select: SelectValueType) -> AsyncRowFactory:
    if isinstance(select, Col):
        return scalar_row
    elif isinstance(select, Sequence):
        return tuple_row
    else:
        return class_row(select)  # type: ignore


def construct_composed_get_query(
        select: SelectValueType,
        from_: FromValueType,
        join: JoinValueType | None,
        where: WhereValueType | None,
        group_by: GroupByValueType | None,
        having: HavingValueType | None,
        order_by: OrderByValueType | None,
        limit: int | None,
        offset: int | None,
) -> Composed:

    query = q.select(select).from_(from_)

    if join:
        query = query.join(join)
    if where:
        query = query.where(where)
    if group_by:
        query = query.group_by(group_by)
    if having:
        query = query.having(having)
    if order_by:
        query = query.order_by(order_by)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    return query.get_composed()


def construct_composed_insert_query(
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        returning: ReturningValueType | None,
        additional_values: AdditionalValuesType | None,
) -> Composed:

    additional_values = additional_values or {}

    query = q.insert_into(insert_into).values(*values, **additional_values)

    if returning:
        query = query.returning(returning)

    return query.get_composed()


def construct_composed_update_query(
        update: UpdateValueType,
        set_: tuple[SetColsType, SetValueType],
        where: WhereValueType | None,
        returning: ReturningValueType | None,
        additional_values: AdditionalValuesType | None,
) -> Composed:

    additional_values = additional_values or {}

    query = q.update(update).set(set_[0], set_[1], **additional_values)

    if where:
        query = query.where(where)
    if returning:
        query = query.returning(returning)

    return query.get_composed()


def construct_composed_delete_query(
        delete_from: DeleteFromValueType,
        using: UsingValueType | None,
        where: WhereValueType | None,
        returning: ReturningValueType | None,
) -> Composed:

    query = q.delete_from(delete_from)

    if using:
        query = query.using(using)
    if where:
        query = query.where(where)
    if returning:
        query = query.returning(returning)

    return query.get_composed()
