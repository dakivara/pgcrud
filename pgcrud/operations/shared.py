from typing import Sequence

from pgcrud.query import Query
from pgcrud.query_builder import QueryBuilder as q
from pgcrud.types import DeleteFromValueType, GroupByValueType, HavingValueType, SelectValueType, FromValueType, SetColsType, SetValuesType, UpdateValueType, UsingValueType, WhereValueType, OrderByValueType, InsertIntoValueType, ValuesValueType, ReturningValueType, AdditionalValuesType, WindowValueType


__all__ = [
    'construct_composed_get_query',
    'construct_composed_insert_query',
    'construct_composed_update_query',
    'construct_composed_delete_query',
]


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
) -> Query:

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

    return query


def construct_composed_insert_query(
        insert_into: InsertIntoValueType,
        values: Sequence[ValuesValueType],
        returning: ReturningValueType | None,
        additional_values: AdditionalValuesType | None,
) -> Query:

    additional_values = additional_values or {}

    query = q.INSERT_INTO(insert_into).VALUES(*values, **additional_values)

    if returning:
        query = query.RETURNING(returning)

    return query


def construct_composed_update_query(
        update: UpdateValueType,
        set_columns: SetColsType,
        set_values: SetValuesType,
        from_: FromValueType | None,
        where: WhereValueType | None,
        returning: ReturningValueType | None,
        additional_values: AdditionalValuesType | None,
) -> Query:

    additional_values = additional_values or {}

    query = q.UPDATE(update).SET(set_columns, set_values, **additional_values)

    if from_:
        query = query.FROM(from_)
    if where:
        query = query.WHERE(where)
    if returning:
        query = query.RETURNING(returning)

    return query


def construct_composed_delete_query(
        delete_from: DeleteFromValueType,
        using: UsingValueType | None,
        where: WhereValueType | None,
        returning: ReturningValueType | None,
) -> Query:

    query = q.DELETE_FROM(delete_from)

    if using:
        query = query.USING(using)
    if where:
        query = query.WHERE(where)
    if returning:
        query = query.RETURNING(returning)

    return query
