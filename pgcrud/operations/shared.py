from collections.abc import Sequence
from typing import Any

from pgcrud.expressions.base import IdentifierExpression
from pgcrud.query import Query
from pgcrud.query_builder import QueryBuilder as q
from pgcrud.utils import ensure_seq


__all__ = [
    'construct_composed_get_query',
    'construct_composed_insert_query',
    'construct_composed_update_query',
    'construct_composed_delete_query',
]


def construct_composed_get_query(
        select: Any | Sequence[Any],
        from_: Any,
        where: Any | None,
        group_by: Any | Sequence[Any] | None,
        having: Any | None,
        window: Any | Sequence[Any] | None,
        order_by: Any | Sequence[Any] | None,
        limit: int | None,
        offset: int | None,
) -> Query:

    query = q.SELECT(*ensure_seq(select)).FROM(from_)

    if where:
        query = query.WHERE(where)
    if group_by:
        query = query.GROUP_BY(*ensure_seq(group_by))
    if having:
        query = query.HAVING(having)
    if window:
        query = query.WINDOW(*ensure_seq(window))
    if order_by:
        query = query.ORDER_BY(*ensure_seq(order_by))
    if limit:
        query = query.LIMIT(limit)
    if offset:
        query = query.OFFSET(offset)

    return query


def construct_composed_insert_query(
        insert_into: IdentifierExpression,
        values: Sequence[Any],
        # on_conflict: Any | None,
        returning: Any | Sequence[Any] | None,
        additional_values: dict[str, Any] | None,
) -> Query:

    additional_values = additional_values or {}

    query = q.INSERT_INTO(insert_into).VALUES(*values, **additional_values)

    # if on_conflict:
    #     query = query.ON_CONFLICT.merge(on_conflict)

    if returning:
        query = query.RETURNING(*ensure_seq(returning))

    return query


def construct_composed_update_query(
        update: Any,
        set_: tuple[IdentifierExpression | Sequence[IdentifierExpression], Any],
        from_: Any | None,
        where: Any | None,
        returning: Any | Sequence[Any] | None,
        additional_values: dict[str, Any] | None,
) -> Query:

    additional_values = additional_values or {}

    query = q.UPDATE(update).SET(set_[0], set_[1], **additional_values)

    if from_:
        query = query.FROM(from_)
    if where:
        query = query.WHERE(where)
    if returning:
        query = query.RETURNING(*ensure_seq(returning))

    return query


def construct_composed_delete_query(
        delete_from: Any,
        using: Any | None,
        where: Any | None,
        returning: Any | Sequence[Any] | None,
) -> Query:

    query = q.DELETE_FROM(delete_from)

    if using:
        query = query.USING(using)
    if where:
        query = query.WHERE(where)
    if returning:
        query = query.RETURNING(*ensure_seq(returning))

    return query
