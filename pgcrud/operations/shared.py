from collections.abc import Sequence
from typing import Any

from psycopg.sql import Composed
from psycopg.rows import scalar_row, tuple_row, class_row, RowFactory, AsyncRowFactory

from pgcrud.expr import Expr
from pgcrud.query_builder import QueryBuilder as q
from pgcrud.types import DeleteFromValueType, GroupByValueType, HavingValueType, SelectValueType, FromValueType, SetValueType, UpdateValueType, UsingValueType, WhereValueType, OrderByValueType, InsertIntoValueType, ValuesValueType, ReturningValueType, AdditionalValuesType, WindowValueType


__all__ = [
    'get_row_factory',
    'get_async_row_factory',
    'construct_composed_get_query',
    'construct_composed_insert_query',
    'construct_composed_update_query',
    'construct_composed_delete_query',
]


def get_row_factory(select: SelectValueType) -> RowFactory[Any]:
    if isinstance(select, Expr):
        return scalar_row
    elif isinstance(select, Sequence):
        return tuple_row
    else:
        return class_row(select)  # type: ignore


def get_async_row_factory(select: SelectValueType) -> AsyncRowFactory[Any]:
    if isinstance(select, Expr):
        return scalar_row
    elif isinstance(select, Sequence):
        return tuple_row
    else:
        return class_row(select)  # type: ignore


def construct_composed_get_query(
        select: SelectValueType,
        from_: FromValueType,
        where: WhereValueType | None,
        group_by: GroupByValueType | None,
        having: HavingValueType | None,
        window: WindowValueType | None,
        order_by: OrderByValueType | None,
        limit: int | None,
        offset: int | None,
) -> Composed:

    query = q.SELECT(select).FROM(from_)

    if where:
        query = query.WHERE(where)
    if group_by:
        query = query.GROUP_BY(group_by)
    if having:
        query = query.HAVING(having)
    if window:
        query = query.WINDOW(window)
    if order_by:
        query = query.ORDER_BY(order_by)
    if limit:
        query = query.LIMIT(limit)
    if offset:
        query = query.OFFSET(offset)

    return query.get_composed()


def construct_composed_insert_query(
        insert_into: InsertIntoValueType,
        values: ValuesValueType,
        returning: ReturningValueType | None,
        additional_values: AdditionalValuesType | None,
) -> Composed:

    additional_values = additional_values or {}

    query = q.INSERT_INTO(insert_into).VALUES(*values, **additional_values)

    if returning:
        query = query.RETURNING(returning)

    return query.get_composed()


def construct_composed_update_query(
        update: UpdateValueType,
        set_: SetValueType,
        from_: FromValueType | None,
        where: WhereValueType | None,
        returning: ReturningValueType | None,
        additional_values: AdditionalValuesType | None,
) -> Composed:

    additional_values = additional_values or {}

    query = q.UPDATE(update).SET(set_[0], set_[1], **additional_values)

    if from_:
        query = query.FROM(from_)
    if where:
        query = query.WHERE(where)
    if returning:
        query = query.RETURNING(returning)

    return query.get_composed()


def construct_composed_delete_query(
        delete_from: DeleteFromValueType,
        using: UsingValueType | None,
        where: WhereValueType | None,
        returning: ReturningValueType | None,
) -> Composed:

    query = q.DELETE_FROM(delete_from)

    if using:
        query = query.USING(using)
    if where:
        query = query.WHERE(where)
    if returning:
        query = query.RETURNING(returning)

    return query.get_composed()
