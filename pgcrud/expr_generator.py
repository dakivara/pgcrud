from pgcrud.expr import ReferenceExpr


__all__ = ['ExprGenerator']


class ExprGeneratorType(type):

    def __getattr__(cls, name) -> ReferenceExpr:
        return ReferenceExpr(name)

    def __call__(cls, name: str) -> ReferenceExpr:
        return ReferenceExpr(name)


class ExprGenerator(metaclass=ExprGeneratorType):
    pass
