from collections.abc import Sequence

from typing import Any

from psycopg.sql import SQL, Composed, Identifier, Placeholder, Literal
from psycopg.rows import scalar_row, tuple_row, dict_row, class_row, RowFactory
from pydantic import BaseModel

from pgcrud._operations.type_hints import *
from pgcrud._star import *


__all__ = [
    'get_row_factory',
    'prepare_select_query',
    'prepare_insert_params',
    'prepare_insert_query',
    'prepare_update_query',
    'prepare_delete_query',
    'prepare_execute_params',
]


def get_row_factory(select: SelectType) -> RowFactory:
    if isinstance(select, str):
        return scalar_row
    elif isinstance(select, tuple) or isinstance(select, _TSTAR):
        return tuple_row
    elif isinstance(select, list) or isinstance(select, _DSTAR):
        return dict_row
    else:
        return class_row(select)  # noqa


def prepare_select_query(
        select: SelectType,
        from_: str,
        where: WhereType | None,
        order_by: OrderByType | None,
        limit: int | None,
        offset: int | None
) -> Composed:

    composed_list = [SQL('SELECT {} FROM {}').format(construct_composed_select(select), Identifier(from_))] # noqa

    if where and (composed_where := construct_composed_where(where)):
        composed_list.append(SQL('WHERE {}').format(composed_where))

    if order_by and (composed_order_by := construct_composed_order_by(order_by)):
        composed_list.append(SQL('ORDER BY {}').format(composed_order_by))

    if limit and (composed_limit := construct_composed_limit(limit)):
        composed_list.append(SQL('LIMIT {}').format(composed_limit))

    if offset and (offset_composed := construct_composed_offset(offset)):
        composed_list.append(SQL('OFFSET {}').format(offset_composed))

    return SQL(' ').join(composed_list)


def prepare_insert_params(values: ValuesType | None, kwargs: dict[str, Any], exclude: ExcludeType | None) -> dict[str, Any]:

    params = kwargs.copy()

    if values:
        if isinstance(values, Sequence):
            params.update(dict(values))
        elif isinstance(values, dict):
            params.update(values)
        else:
            params.update(values.model_dump(by_alias=True, exclude=set(exclude) if isinstance(exclude, list) else {exclude}))

    return params


def prepare_insert_query(insert_into: str, params: dict[str, Any], returning: SelectType | None) -> Composed:

    composed_list = [SQL('INSERT INTO {} ({}) VALUES ({})').format(Identifier(insert_into), construct_composed_columns(params), construct_composed_placeholders(params))]

    if returning:
        composed_list.append(SQL('RETURNING {}').format(construct_composed_select(returning)))

    return SQL(' ').join(composed_list)


def prepare_update_query(update: str, set_: SetType, where: WhereType | None, returning: SelectType | None, exclude: ExcludeType | None, kwargs: dict[str, Any]) -> Composed:

    composed_list = [SQL('UPDATE {} SET {}').format(Identifier(update), construct_composed_set(set_, kwargs, exclude))]

    if where and (composed_where := construct_composed_where(where)):
        composed_list.append(SQL('WHERE {}').format(composed_where))

    if returning:
        composed_list.append(SQL('RETURNING {}').format(construct_composed_select(returning)))

    return SQL(' ').join(composed_list)


def prepare_delete_query(delete_from: str, where: WhereType | None, returning: SelectType | None) -> Composed:

    composed_list = [SQL('DELETE FROM {}').format(Identifier(delete_from))]

    if where and (composed_where := construct_composed_where(where)):
        composed_list.append(SQL('WHERE {}').format(composed_where))

    if returning:
        composed_list.append(SQL('RETURNING {}').format(construct_composed_select(returning)))

    return SQL(' ').join(composed_list)


def prepare_execute_params(params: ParamsType | None) -> tuple[Any] | dict[str, Any] | None:

    if params:
        if isinstance(params, BaseModel):
            params = params.model_dump(by_alias=True)

    return params


def construct_composed_select(select: SelectType) -> Composed:
    if isinstance(select, str):
        return Composed([Identifier(select)])
    elif isinstance(select, tuple) or isinstance(select, list):
        return SQL(', ').join([Identifier(name) for name in select])
    elif isinstance(select, _TSTAR) or isinstance(select, _DSTAR):
        return Composed([SQL('*')])
    else:
        return SQL(', ').join([Identifier(field.validation_alias or name) for name, field in select.model_fields.items()])


def construct_composed_where(where: WhereType) -> Composed | None:
    if isinstance(where, list):
        composed_list = [composed for operator in where if (composed := operator.get_composed())]
        if composed_list:
            return SQL(' AND ').join(composed_list)
    else:
        return where.get_composed()


def construct_composed_order_by(order_by: OrderByType) -> Composed | None:
    if isinstance(order_by, list):
        composed_list = [composed for operator in order_by if (composed := operator.get_composed())]
        if composed_list:
            return SQL(', ').join(composed_list)
    else:
        return order_by.get_composed()


def construct_composed_set(set_: SetType, kwargs: dict[str, Any], exclude: ExcludeType | None) -> Composed:

    params = kwargs.copy()

    if isinstance(set_, list):
        params.update(dict(set_))
    elif isinstance(set_, dict):
        params.update(set_)
    else:
        params.update(set_.model_dump(by_alias=True, exclude=set(exclude) if isinstance(exclude, list) else {exclude}))

    return SQL(', ').join([SQL("{} = {}").format(Identifier(key), Literal(value)) for key, value in params.items()])


def construct_composed_limit(limit: int) -> Composed:
    return Composed([Literal(limit)])


def construct_composed_offset(offset: int) -> Composed:
    return Composed([Literal(offset)])


def construct_composed_columns(params: dict[str, Any]) -> Composed:
    return SQL(', ').join([Identifier(column) for column in params])


def construct_composed_placeholders(params: dict[str, Any]) -> Composed:
    return SQL(', ').join(Placeholder(column) for column in params)
