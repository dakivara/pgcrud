from typing import TYPE_CHECKING

from pgcrud.col import ToJsonCol


if TYPE_CHECKING:
    from pgcrud.tab import Tab


def to_json(tab: 'Tab') -> ToJsonCol:
    return ToJsonCol(tab)
