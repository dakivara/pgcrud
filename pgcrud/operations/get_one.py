from collections.abc import Sequence
from typing import Any

from pgcrud.db.cursor import Cursor, ServerCursor
from pgcrud.operations.shared import construct_composed_get_query
from pgcrud.types import Row


def get_one(
        cursor: Cursor[Row] | ServerCursor[Row],
        select: Any | Sequence[Any],
        from_: Any,
        *,
        where: Any | None = None,
        group_by: Any | Sequence[Any] | None = None,
        having: Any | None = None,
        window: Any | Sequence[Any] | None = None,
        order_by: Any | Sequence[Any] | None = None,
        offset: int | None = None,
) -> Row | None:

    query = construct_composed_get_query(select, from_, where, group_by, having, window, order_by, 1, offset)
    cursor.execute(query)

    return cursor.fetchone()
