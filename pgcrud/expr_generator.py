from pgcrud.expr import ReferenceExpr


__all__ = ['ExprGenerator']

from pgcrud.frame_boundaries import CurrentRow, UnboundedFollowing, UnboundedPreceding


class ExprGeneratorType(type):

    def __getattr__(cls, name) -> ReferenceExpr:
        return ReferenceExpr(name)

    def __call__(cls, name: str) -> ReferenceExpr:
        return ReferenceExpr(name)

    @property
    def UNBOUNDED_PRECEDING(cls) -> UnboundedPreceding:
        return UnboundedPreceding()

    @property
    def UNBOUNDED_FOLLOWING(cls) -> UnboundedFollowing:
        return UnboundedFollowing()

    @property
    def CURRENT_ROW(cls) -> CurrentRow:
        return CurrentRow()


class ExprGenerator(metaclass=ExprGeneratorType):
    pass
