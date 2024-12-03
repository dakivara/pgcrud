from collections.abc import Sequence
from typing import TypeVar


__all__ = ['ensure_seq']


T = TypeVar('T')


def ensure_seq(value: T | Sequence[T]) -> Sequence[T]:
    if isinstance(value, Sequence):
        return value
    else:
        return [value]
