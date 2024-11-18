from typing import Any, Literal, overload

from psycopg import Cursor

from pgcrud._operations.type_hints import *
from pgcrud._operations.utils import *
from pgcrud._star import *


@overload
def get_many(cursor: Cursor, select: str, from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[False] = False) -> list[Any]: ...


@overload
def get_many(cursor: Cursor, select: tuple[str] | _TSTAR, from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[False] = False) -> list[tuple[Any, ...]]: ...


@overload
def get_many(cursor: Cursor, select: list[str] | _DSTAR, from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[False] = False) -> list[dict[str, Any]]: ...


@overload
def get_many(cursor: Cursor, select: type[OutputModel], from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[False] = False) -> list[OutputModel]: ...


@overload
def get_many(cursor: Cursor, select: SelectType, from_: str, *, where: WhereType = None, order_by: OrderByType = None, limit: int = None, offset: int = None, no_fetch: Literal[True] = False) -> None: ...


def get_many(
        cursor: Cursor,
        select: SelectType,
        from_: str,
        *,
        where: WhereType = None,
        order_by: OrderByType = None,
        limit: int = None,
        offset: int = None,
        no_fetch: bool = False,
) -> list[ReturnType] | None:
    """
    Retrieves multiple records from a database table based on the specified query parameters and returns them as a list.

    :param cursor: The database cursor object used to execute the query.
    :type cursor: Cursor
    :param select: The fields or expressions to retrieve in the SELECT clause.
    :type select: SelectType
    :param from_: The name of the database table to query.
    :type from_: str
    :param where: Filtering conditions for the WHERE clause (optional).
    :type where: WhereType, optional
    :param order_by: Sorting criteria for the ORDER BY clause (optional).
    :type order_by: OrderByType, optional
    :param limit: Maximum number of records to return (LIMIT clause, optional).
    :type limit: int, optional
    :param offset: The starting point for records to return (OFFSET clause, optional).
    :type offset: int, optional
    :param no_fetch: If True, executes the query without fetching results. Defaults to False.
    :type no_fetch: bool, optional

    :returns: A list of records matching the query, or None if no_fetch is True.
    :rtype: list[ReturnType] | None
    """

    cursor.row_factory = get_row_factory(select)
    query = prepare_select_query(select, from_, where, order_by, limit, offset)
    cursor.execute(query)

    if not no_fetch:
        return cursor.fetchall()
