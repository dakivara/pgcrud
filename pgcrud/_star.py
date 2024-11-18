
__all__ = [
    '_TSTAR',
    '_DSTAR',
]


class _TSTAR:

    def __repr__(self):
        return "*"

    def __eq__(self, other):
        return isinstance(other, _TSTAR)


class _DSTAR:

    def __repr__(self):
        return "*"

    def __eq__(self, other):
        return isinstance(other, _DSTAR)


TSTAR = _TSTAR()
DSTAR = _DSTAR()
