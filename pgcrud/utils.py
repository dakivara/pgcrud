from typing import Any

from pgcrud.types import SequenceType


__all__ = ['ensure_seq']


def ensure_seq(value: Any | SequenceType) -> SequenceType:
    if isinstance(value, SequenceType):
        return value
    else:
        return [value]
