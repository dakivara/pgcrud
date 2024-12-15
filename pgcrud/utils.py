from collections.abc import Sequence

from pgcrud.types import T


__all__ = ['ensure_seq']


def ensure_seq(value: T | Sequence[T]) -> Sequence[T]:
    if isinstance(value, Sequence):
        return value
    else:
        return [value]
