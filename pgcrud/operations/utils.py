from collections.abc import Sequence
from typing import Any

from psycopg.sql import SQL, Composed, Identifier, Literal
from psycopg.rows import scalar_row, tuple_row, class_row, RowFactory, AsyncRowFactory
from pydantic import BaseModel

from pgcrud.col import SingleCol, Col
from pgcrud.operators.assign import Assign
from pgcrud.operations.type_hints import *
from pgcrud.query_builder import QueryBuilder as q
from pgcrud.tab import SimpleTab
from pgcrud.types import DeleteFromValueType, SelectValueType, FromValueType, JoinValueType, SetColsType, SetValueType, UpdateValueType, WhereValueType, OrderByValueType, InsertIntoValueType, ValuesValueType, ReturningValueType, AdditionalValuesType


__all__ = [
    'get_row_factory',
    'get_async_row_factory',
    'construct_composed_get_query',
    'construct_composed_insert_query',
    'construct_composed_update_query',
    'construct_composed_delete_query',
    'prepare_select_query',
    'prepare_insert_params',
    'prepare_insert_query',
    'prepare_update_query',
    'prepare_delete_query',
    'prepare_execute_params',
    'prepare_execute_params_seq',
]


def get_row_factory(select: SelectType) -> RowFactory:
    if isinstance(select, str) or isinstance(select, Col):
        return scalar_row
    elif isinstance(select, Sequence):
        return tuple_row
    else:
        return class_row(select)  # type: ignore


def get_async_row_factory(select: SelectType) -> AsyncRowFactory:
    if isinstance(select, str) or isinstance(select, Col):
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
        order_by: OrderByValueType | None,
        limit: int | None,
        offset: int | None,
) -> Composed:

    query = q.select(select).from_(from_)

    if join:
        query = query.join(join)
    if where:
        query = query.where(where)
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
        where: WhereValueType | None,
        returning: ReturningValueType | None,
) -> Composed:

    query = q.delete_from(delete_from)

    if where:
        query = query.where(where)
    if returning:
        query = query.returning(returning)

    return query.get_composed()


def prepare_select_query(
        select: SelectType,
        from_: TableType,
        join: None,
        where: WhereType | None,
        order_by: OrderByType | None,
        limit: int | None,
        offset: int | None,
) -> Composed:

    composed_select = construct_composed_select(select)
    composed_from = construct_composed_table(from_)

    composed_list = [SQL('SELECT {} FROM {}').format(composed_select, composed_from)]   # type: ignore

    if composed_join := construct_composed_join(join):
        composed_list.append(composed_join)

    if composed_where := construct_composed_where(where):
        composed_list.append(SQL('WHERE {}').format(composed_where))

    if composed_order_by := construct_composed_order_by(order_by):
        composed_list.append(SQL('ORDER BY {}').format(composed_order_by))

    if composed_limit := construct_composed_limit(limit):
        composed_list.append(SQL('LIMIT {}').format(composed_limit))

    if composed_offset := construct_composed_offset(offset):
        composed_list.append(SQL('OFFSET {}').format(composed_offset))

    return SQL(' ').join(composed_list)


def prepare_insert_params(values: ValuesType, additional_values: dict[str, Any] | None, exclude: ExcludeType | None) -> dict[str, Any]:

    params = {}

    if isinstance(values, dict):
        params.update(values)
    else:
        params.update(values.model_dump(by_alias=True))

    if exclude:
        if isinstance(exclude, str):
            exclude = [exclude]

        for key in exclude:
            params.pop(key, None)

    if additional_values:
        params.update(additional_values)

    return params


def prepare_insert_query(insert_into: TableType, params: list[dict[str, Any]], returning: SelectType | None) -> Composed:

    composed_insert_into = construct_composed_table(insert_into)
    composed_columns = construct_composed_columns(params[0])
    composed_values = construct_composed_values(params)

    composed_list = [SQL('INSERT INTO {} ({}) VALUES {}').format(composed_insert_into, composed_columns, composed_values)]  # type: ignore

    if returning and (composed_returning := construct_composed_select(returning)):
        composed_list.append(SQL('RETURNING {}').format(composed_returning))

    return SQL(' ').join(composed_list)


def prepare_update_query(update: TableType, set_: SetType, where: WhereType | None, returning: SelectType | None, exclude: ExcludeType | None) -> Composed:

    composed_table = construct_composed_table(update)
    composed_set = construct_composed_set(set_, exclude)

    composed_list = [SQL('UPDATE {} SET {}').format(composed_table, composed_set)]  # type: ignore

    if composed_where := construct_composed_where(where):
        composed_list.append(SQL('WHERE {}').format(composed_where))

    if returning and (composed_returning := construct_composed_select(returning)):
        composed_list.append(SQL('RETURNING {}').format(composed_returning))

    return SQL(' ').join(composed_list)


def prepare_delete_query(delete_from: TableType, where: WhereType | None, returning: SelectType | None) -> Composed:

    composed_table = construct_composed_table(delete_from)

    composed_list = [SQL('DELETE FROM {}').format(composed_table)]  # type: ignore

    if composed_where := construct_composed_where(where):
        composed_list.append(SQL('WHERE {}').format(composed_where))

    if returning and (composed_returning := construct_composed_select(returning)):
        composed_list.append(SQL('RETURNING {}').format(composed_returning))

    return SQL(' ').join(composed_list)


def prepare_execute_params(params: ParamsType | None) -> Sequence[Any] | dict[str, Any] | None:

    if params:
        if isinstance(params, BaseModel):
            params = params.model_dump(by_alias=True)

    return params


def prepare_execute_params_seq(params: Sequence[ParamsType]) -> list[Sequence[Any] | dict[str, Any]]:
    return [p.model_dump(by_alias=True) if isinstance(p, BaseModel) else p for p in params]


def construct_composed_table(table: TableType) -> Composed:
    return table.get_composed()


def construct_composed_select(select: SelectType) -> Composed:
    if isinstance(select, str):
        return SingleCol(select).get_composed()
    elif isinstance(select, Col):
        return select.get_composed()
    elif isinstance(select, Sequence):
        return SQL(', ').join([SingleCol(v).get_composed() if isinstance(v, str) else v.get_composed() for v in select])
    else:
        composed_list = []

        for name, field in select.model_fields.items():
            col = SingleCol(name)

            for m in field.metadata:
                if isinstance(m, Col):
                    col = m
                    break

            composed_list.append(col.get_composed())

        return SQL(', ').join(composed_list)


def construct_composed_join(join: None) -> Composed | None:
    if join:
        if not isinstance(join, Sequence):
            join = [join]
        return SQL(' ').join([j.get_composed() for j in join])


def construct_composed_where(where: WhereType | None) -> Composed | None:
    if where:
        return where.get_composed()


def construct_composed_order_by(order_by: OrderByType | None) -> Composed | None:
    if order_by:

        if not isinstance(order_by, Sequence):
            order_by = [order_by]

        # order_by = CompositeSort([operator.asc() if isinstance(operator, Col) else operator for operator in order_by])
        #
        # if order_by:
        #     return order_by.get_composed()


def construct_composed_set(set_: SetType, exclude: ExcludeType | None) -> Composed:

    composed_list = []
    params = {}

    if not isinstance(set_, Sequence):
        set_ = [set_]

    for s in set_:
        if isinstance(s, Assign):
            composed_list.append(s.get_composed())
        elif isinstance(s, dict):
            params.update(s)
        else:
            params.update(s.model_dump(by_alias=True))

    if exclude:
        if isinstance(exclude, str):
            exclude = [exclude]

        for key in exclude:
            params.pop(key, None)

    for key, value in params.items():
        composed_list.append(SQL('{} = {}').format(Identifier(key), Literal(value)))

    return SQL(', ').join(composed_list)


def construct_composed_limit(limit: int | None) -> Composed | None:
    if limit:
        return Composed([Literal(limit)])


def construct_composed_offset(offset: int | None) -> Composed | None:
    if offset:
        return Composed([Literal(offset)])


def construct_composed_columns(params: dict[str, Any]) -> Composed:
    return SQL(', ').join([Identifier(key) for key in params])


def construct_composed_values(params: list[dict[str, Any]]) -> Composed:
    composed_values_list = []

    for p in params:
        composed_values_list.append(Composed([SQL('('), SQL(', ').join([Literal(value) for value in p.values()]), SQL(')')]))

    return SQL(', ').join(composed_values_list)
